"""Pre-flight diagnostic: run the guardrail on the GOLD queries of a dev set.

This needs no API key. It answers a question worth knowing before spending money on
generation: how many gold (correct) queries does our guardrail itself accept? That is
the ceiling the `wrapped` mode can reach, and the block reasons explain where the
guardrail is stricter than Spider (e.g. joins outside declared foreign keys).

Run inside the `api` image (it has sqlglot). See README.md.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "services" / "api"))

from app.sql_guardrails import SQLValidationError, validate_gold_select  # noqa: E402

from schema_adapter import load_spider_schemas  # noqa: E402
from sqlnorm import to_lower_identifiers  # noqa: E402

HUGE_LIMIT = 1_000_000_000


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", required=True)
    parser.add_argument("--tables", required=True)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    schemas = load_spider_schemas(args.tables)
    dev = json.loads(Path(args.dev).read_text(encoding="utf-8"))
    if args.limit:
        dev = dev[: args.limit]

    passed = blocked = parse_err = missing = 0
    blocked_with_doublequote = 0
    reasons: dict[str, int] = {}
    examples: dict[str, str] = {}
    for ex in dev:
        schema = schemas.get(ex["db_id"])
        if schema is None:
            missing += 1
            continue
        try:
            validate_gold_select(to_lower_identifiers(ex["query"]), schema, HUGE_LIMIT)
            passed += 1
        except SQLValidationError as exc:
            blocked += 1
            if '"' in ex["query"]:
                blocked_with_doublequote += 1
            key = str(exc).split(":")[0][:48]
            reasons[key] = reasons.get(key, 0) + 1
            examples.setdefault(key, ex["query"])
        except Exception as exc:  # noqa: BLE001
            parse_err += 1
            key = "PARSE_ERROR: " + type(exc).__name__
            reasons[key] = reasons.get(key, 0) + 1
            examples.setdefault(key, ex["query"])

    n = len(dev)
    print(f"GOLD-vs-GUARDRAIL on {n} examples:")
    print(f"  passed     = {passed} ({passed / n:.1%})  <- ceiling for wrapped exec_acc")
    print(f"  blocked    = {blocked} ({blocked / n:.1%})")
    print(f"  parse_err  = {parse_err}")
    print(f"  missing_db = {missing}")
    print(f"  of blocked, contain a double-quote literal (Spider quirk, not a real block) = {blocked_with_doublequote}")
    print("\nTop block reasons:")
    for key, count in sorted(reasons.items(), key=lambda kv: -kv[1])[:10]:
        print(f"  {count:4d}  {key}")
        print(f"         e.g. {examples[key][:90]}")


if __name__ == "__main__":
    main()
