"""Run the Text-to-SQL wrapper over a Spider/BIRD dev set and score it.

Two modes, for the ablation the advisor asked for:
- `baseline`: gpt-4.1-mini generates SQL from the raw schema. No guardrail, no repair.
- `wrapped` : same model + schema-grounded prompt + the project's `validate_gold_select`
              guardrail + one guarded repair on failure.

The delta (wrapped - baseline) isolates the contribution of the wrapper. Both modes
get the full schema, so the comparison is fair; only the grounding structure +
guardrail + repair differ.

NOTE: the taxi-specific deterministic planner in `app.agent` is intentionally NOT
used here. It only covers the taxi domain; this harness measures the general
text-to-SQL capability (LLM + guardrail), which is what generalizes to Spider/BIRD.

Run inside the `api` container (it has openai + sqlglot), with the Spider data
reachable. See README.md.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "services" / "api"))

from app.models import SchemaResponse  # noqa: E402
from app.sql_guardrails import SQLValidationError, validate_gold_select  # noqa: E402

from schema_adapter import load_spider_schemas  # noqa: E402
from scorer import score_prediction  # noqa: E402
from sqlnorm import to_lower_identifiers  # noqa: E402

HUGE_LIMIT = 1_000_000_000  # neutralizes the guardrail's LIMIT injection for exact result match

_FENCE = re.compile(r"```(?:sql)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)


def _extract_sql(content: str) -> str:
    stripped = (content or "").strip()
    fenced = _FENCE.search(stripped)
    if fenced:
        stripped = fenced.group(1).strip()
    return stripped.rstrip(";").strip()


def render_schema(schema: SchemaResponse, *, with_joins: bool) -> str:
    lines: list[str] = []
    for table in schema.tables:
        cols = ", ".join(field.name for field in table.fields)
        lines.append(f"Table {table.name}({cols})")
    if with_joins:
        joins = [
            f"  {j.left_table}.{j.left_column} = {j.right_table}.{j.right_column}"
            for table in schema.tables
            for j in table.allowed_joins
        ]
        if joins:
            lines.append("Foreign-key join paths:")
            lines.extend(joins)
    return "\n".join(lines)


def _call_openai(client, model: str, system: str, user: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
    )
    return _extract_sql(response.choices[0].message.content or "")


BASELINE_SYSTEM = (
    "You are a Text-to-SQL generator for SQLite. "
    "Return exactly one SELECT statement and no prose. "
    "Use single quotes for string literals."
)
WRAPPED_SYSTEM = (
    "You are a Text-to-SQL generator for SQLite. "
    "Return exactly one SELECT statement and no prose. "
    "Use only the tables and columns listed in the schema. Do not invent columns. "
    "Join tables only along the listed foreign-key join paths. "
    "Use single quotes for string literals."
)
REPAIR_SYSTEM = (
    "Repair one SQLite SELECT query. Return exactly one SELECT statement and no prose. "
    "Use only the listed tables, columns, and foreign-key join paths. "
    "Use single quotes for string literals."
)


def generate_baseline(client, model, schema, question) -> str:
    user = f"Schema:\n{render_schema(schema, with_joins=False)}\n\nQuestion: {question}"
    return _call_openai(client, model, BASELINE_SYSTEM, user)


def generate_wrapped(client, model, schema, question, catalog) -> dict:
    """Generate -> validate -> one repair. Returns dict with sql, blocked flag, repaired flag."""
    schema_text = render_schema(schema, with_joins=True)
    user = f"Schema:\n{schema_text}\n\nQuestion: {question}"
    candidate = _call_openai(client, model, WRAPPED_SYSTEM, user)

    # Validate on case-normalized identifiers (matches the lowercased catalog); execute
    # the original SQL (SQLite is case-insensitive).
    try:
        validate_gold_select(to_lower_identifiers(candidate), catalog, HUGE_LIMIT)
        return {"sql": candidate, "blocked": False, "repaired": False}
    except SQLValidationError as exc:
        repair_user = (
            f"Schema:\n{schema_text}\n\nQuestion: {question}\n"
            f"Rejected SQL: {candidate}\nGuardrail error: {exc}"
        )
        repaired = _call_openai(client, model, REPAIR_SYSTEM, repair_user)
        try:
            validate_gold_select(to_lower_identifiers(repaired), catalog, HUGE_LIMIT)
            return {"sql": repaired, "blocked": False, "repaired": True}
        except SQLValidationError:
            return {"sql": repaired, "blocked": True, "repaired": True}


def db_path_for(db_dir: Path, db_id: str) -> str:
    return str(db_dir / db_id / f"{db_id}.sqlite")


def run(args) -> None:
    from openai import OpenAI

    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or api_key == "replace-me":
        raise SystemExit("OPENAI_API_KEY is not configured.")
    client = OpenAI(api_key=api_key)

    schemas = load_spider_schemas(args.tables)
    dev = json.loads(Path(args.dev).read_text(encoding="utf-8"))
    if args.stride > 1:
        dev = dev[:: args.stride]  # spread the sample across databases/difficulties
    if args.limit:
        dev = dev[: args.limit]
    db_dir = Path(args.db_dir)

    modes = ["baseline", "wrapped"] if args.mode == "both" else [args.mode]
    out = Path(args.out)
    results: dict[str, list] = {mode: [] for mode in modes}
    done: dict[str, set] = {mode: set() for mode in modes}
    if args.resume and out.exists():
        prior = json.loads(out.read_text(encoding="utf-8"))
        for mode in modes:
            for rec in prior.get(mode, []):
                results[mode].append(rec)
                done[mode].add((rec.get("db_id"), rec.get("question")))
        print(f"resume: loaded {sum(len(v) for v in done.values())} prior results from {out}")

    def checkpoint() -> None:  # ponytail: crash-safety — a paid run must never lose everything
        out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    for i, ex in enumerate(dev):
        db_id, question, gold = ex["db_id"], ex["question"], ex["query"]
        schema = schemas.get(db_id)
        if schema is None:
            continue
        dbp = db_path_for(db_dir, db_id)
        for mode in modes:
            if (db_id, question) in done[mode]:
                continue
            try:
                if mode == "baseline":
                    pred_sql, blocked, repaired = generate_baseline(client, args.model, schema, question), False, False
                else:
                    gen = generate_wrapped(client, args.model, schema, question, schema)
                    pred_sql, blocked, repaired = gen["sql"], gen["blocked"], gen["repaired"]
            except Exception as exc:  # noqa: BLE001
                results[mode].append({"db_id": db_id, "question": question, "gen_error": str(exc), "correct": False})
                done[mode].add((db_id, question))
                continue

            score = score_prediction(dbp, pred_sql, gold)
            results[mode].append(
                {
                    "db_id": db_id,
                    "question": question,
                    "gold": gold,
                    "pred": pred_sql,
                    "blocked": blocked,
                    "repaired": repaired,
                    **score,
                }
            )
            done[mode].add((db_id, question))
        if (i + 1) % 25 == 0:
            print(f"...{i + 1}/{len(dev)} examples")
            checkpoint()

    checkpoint()
    print(f"\nWrote per-example results to {out}")

    # One predicted SQL per line, in dev order, for the official Spider evaluator.
    # (Assumes no examples were skipped, true for Spider dev where every db_id resolves.)
    for mode, items in results.items():
        pred_path = out.with_name(out.stem + f".pred_{mode}.sql")
        lines = [" ".join((r.get("pred") or "SELECT 1").split()) for r in items]
        pred_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Wrote {len(lines)} predictions to {pred_path}")
    print()
    print(summarize(results))


def summarize(results: dict[str, list]) -> str:
    lines = ["mode      | n    | exec_acc | valid_rate | blocked"]
    lines.append("-" * 52)
    for mode, items in results.items():
        scored = [r for r in items if not r.get("gold_error")]
        n = len(scored)
        if n == 0:
            lines.append(f"{mode:<9} | 0    | n/a")
            continue
        acc = sum(1 for r in scored if r.get("correct")) / n
        valid = sum(1 for r in scored if r.get("valid")) / n
        blocked = sum(1 for r in scored if r.get("blocked")) / n
        lines.append(f"{mode:<9} | {n:<4} | {acc:8.1%} | {valid:10.1%} | {blocked:.1%}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Text-to-SQL wrapper on Spider/BIRD.")
    parser.add_argument("--dev", required=True, help="Path to dev.json")
    parser.add_argument("--tables", required=True, help="Path to tables.json")
    parser.add_argument("--db-dir", required=True, help="Directory of <db_id>/<db_id>.sqlite databases")
    parser.add_argument("--mode", choices=["baseline", "wrapped", "both"], default="both")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    parser.add_argument("--stride", type=int, default=1, help="Take every Nth example (spreads across DBs)")
    parser.add_argument("--limit", type=int, default=0, help="Cap to the first N (after stride; 0 = all)")
    parser.add_argument("--out", default="benchmarks/spider/results.json")
    parser.add_argument("--resume", action="store_true", help="Skip examples already saved in --out (continue a dead run without re-paying)")
    run(parser.parse_args())


if __name__ == "__main__":
    main()
