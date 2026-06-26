"""Execute the taxi gold SQL against the warehouse to confirm each returns rows.

Uses the project's read-only DuckDB engine (configures S3/MinIO from env if present).
Reports, per query, whether it executed and how many rows came back, plus any error.
Some gold queries touch dim_zone/gold_zone_demand, which are views over MinIO; those
need MinIO reachable.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "services" / "api"))

from app.query_engine import QueryExecutionError, execute_readonly_query  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="warehouse/analytics.duckdb")
    parser.add_argument("--questions", default="benchmarks/taxi/taxi_questions.json")
    args = parser.parse_args()

    items = json.loads(Path(args.questions).read_text(encoding="utf-8"))
    ok = 0
    empty = 0
    failures = []
    for item in items:
        try:
            columns, rows, _ = execute_readonly_query(item["query"], args.db)
            if rows:
                ok += 1
            else:
                empty += 1
                print(f"  EMPTY id={item['id']}: {item['question'][:60]}")
        except (QueryExecutionError, Exception) as exc:  # noqa: BLE001
            failures.append((item["id"], item.get("tables"), str(exc)[:120]))

    print(f"\ntaxi gold execution: ran_with_rows={ok}, ran_empty={empty}, failed={len(failures)} of {len(items)}")
    for qid, tables, reason in failures:
        print(f"  FAIL id={qid} tables={tables}: {reason}")


if __name__ == "__main__":
    main()
