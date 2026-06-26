"""Validate the taxi gold SQL against the real semantic catalog + guardrail.

Confirms each hand-written gold query uses cataloged tables/columns/joins and passes
`validate_gold_select` (no data needed). Catches typos before we run the full taxi eval
against the warehouse. Run inside the `api` image.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "services" / "api"))

from app.catalog import load_schema_catalog  # noqa: E402
from app.sql_guardrails import SQLValidationError, validate_gold_select  # noqa: E402

HUGE_LIMIT = 1_000_000_000


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", default="contracts/semantic_catalog.yaml")
    parser.add_argument("--questions", default="benchmarks/taxi/taxi_questions.json")
    args = parser.parse_args()

    catalog = load_schema_catalog(Path(args.catalog))
    items = json.loads(Path(args.questions).read_text(encoding="utf-8"))

    ok = 0
    failures = []
    for item in items:
        try:
            validate_gold_select(item["query"], catalog, HUGE_LIMIT)
            ok += 1
        except SQLValidationError as exc:
            failures.append((item["id"], str(exc)))
        except Exception as exc:  # noqa: BLE001
            failures.append((item["id"], f"PARSE: {exc}"))

    print(f"taxi gold vs catalog/guardrail: {ok}/{len(items)} passed")
    for qid, reason in failures:
        print(f"  FAIL id={qid}: {reason}")


if __name__ == "__main__":
    main()
