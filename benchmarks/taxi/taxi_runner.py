"""Run the real agent over the taxi domain questions and score against gold.

Unlike the Spider harness, this uses the full production agent (run_query_agent):
deterministic planner + LLM fallback + guardrail + execution on the warehouse. It
measures the system's real domain accuracy — "does the agent answer taxi questions
correctly", which is what the title and advisor requirement #2 are about.

Scoring: execution-result match. Result rows are compared as a value-multiset that
ignores column order/name (lenient on output shape, strict on values) — see notes.
Run inside the `api` service on the compose network (needs MinIO for zone tables).
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "services" / "api"))

from app.agent import run_query_agent  # noqa: E402
from app.catalog import load_schema_catalog  # noqa: E402
from app.models import QueryRequest  # noqa: E402
from app.query_engine import execute_readonly_query  # noqa: E402

from scoring import is_ordered, values_match  # noqa: E402


def step_source(steps) -> str:
    for step in steps:
        if step.name == "sql_generation":
            return step.metadata.get("source", step.status)
    return "unknown"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", default="contracts/semantic_catalog.yaml")
    parser.add_argument("--questions", default="benchmarks/taxi/taxi_questions.json")
    parser.add_argument("--db", default="/work/warehouse/analytics.duckdb")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    parser.add_argument("--out", default="benchmarks/taxi/taxi_results.json")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY", "")
    catalog = load_schema_catalog(Path(args.catalog))
    items = json.loads(Path(args.questions).read_text(encoding="utf-8"))

    results = []
    for item in items:
        gold_cols, gold_rows, _ = execute_readonly_query(item["query"], args.db)
        rec = {"id": item["id"], "difficulty": item["difficulty"], "question": item["question"],
               "gold_sql": item["query"], "n_gold": len(gold_rows)}
        try:
            response = run_query_agent(
                request=QueryRequest(question=item["question"], max_rows=1000),
                catalog=catalog, model=args.model, api_key=api_key, duckdb_path=args.db,
            )
            rec["agent_sql"] = response.sql
            rec["clarified"] = response.requires_clarification
            rec["source"] = step_source(response.agent_steps)
            rec["n_agent"] = len(response.rows)
            ordered = is_ordered(item["query"])
            rec["ordered"] = ordered
            rec["cols_ok"] = set(gold_cols).issubset(set(response.columns))
            rec["match"] = (not response.requires_clarification) and values_match(
                response.rows, response.columns, gold_rows, gold_cols, ordered)
            rec["agent_cols"] = list(response.columns)
            rec["agent_rows"] = response.rows[:200]  # ponytail: cap for file size; re-scoring needs no more
            rec["gold_cols"] = list(gold_cols)
            rec["gold_rows"] = gold_rows[:200]
        except Exception as exc:  # noqa: BLE001
            rec["agent_error"] = str(exc)[:200]
            rec["match"] = False
        results.append(rec)

    Path(args.out).write_text(
        json.dumps(results, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {args.out}\n")

    answered = [r for r in results if not r.get("clarified") and not r.get("agent_error")]
    matched = [r for r in results if r.get("match")]
    print(f"taxi domain eval: {len(results)} questions")
    print(f"  answered (no clarify / no error) = {len(answered)} ({len(answered)/len(results):.1%})")
    print(f"  result match (accuracy)          = {len(matched)} ({len(matched)/len(results):.1%})")
    for diff in ("easy", "medium", "hard"):
        sub = [r for r in results if r["difficulty"] == diff]
        if sub:
            acc = sum(1 for r in sub if r.get("match")) / len(sub)
            print(f"    {diff:<7}: {acc:.1%} ({sum(1 for r in sub if r.get('match'))}/{len(sub)})")
    # which generation path the agent used
    srcs = Counter(r.get("source", "error") for r in results)
    print(f"  generation source mix: {dict(srcs)}")


if __name__ == "__main__":
    main()
