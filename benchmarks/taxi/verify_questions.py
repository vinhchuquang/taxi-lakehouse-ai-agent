"""Verify candidate gold SQL executes and returns rows on the warehouse, then optionally
merge into taxi_questions.json. Run inside the api service (needs MinIO for zone/fact).

  verify only:  python benchmarks/taxi/verify_questions.py --new new_questions.json
  verify+merge: python benchmarks/taxi/verify_questions.py --new new_questions.json --merge
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "services" / "api"))
from app.query_engine import execute_readonly_query  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", required=True)
    ap.add_argument("--base", default="benchmarks/taxi/taxi_questions.json")
    ap.add_argument("--db", default="/work/warehouse/analytics.duckdb")
    ap.add_argument("--merge", action="store_true")
    args = ap.parse_args()

    new = json.loads(Path(args.new).read_text(encoding="utf-8"))
    bad = []
    for q in new:
        try:
            _, rows, _ = execute_readonly_query(q["query"], args.db)
            n = len(rows)
            status = "OK" if n > 0 else "EMPTY"
            if n == 0:
                bad.append((q["id"], "empty result"))
        except Exception as exc:  # noqa: BLE001
            status, n = "ERROR", 0
            bad.append((q["id"], str(exc)[:120]))
        print(f"  id{q['id']:>3} {q['difficulty']:<6} {status:<6} rows={n:<5} {q['question'][:55]}")

    print(f"\n{len(new) - len(bad)}/{len(new)} verified OK")
    if bad:
        print("PROBLEMS:")
        for i, msg in bad:
            print(f"  id{i}: {msg}")

    if args.merge:
        if bad:
            print("\nNOT merging: fix problems first.")
            return
        base = json.loads(Path(args.base).read_text(encoding="utf-8"))
        combined = base + new
        Path(args.base).write_text(
            json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nMerged -> {args.base}: {len(base)} + {len(new)} = {len(combined)} questions")


if __name__ == "__main__":
    main()
