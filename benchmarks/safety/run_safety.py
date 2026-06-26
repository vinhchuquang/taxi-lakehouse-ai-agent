"""Measure the guardrail's safety on an adversarial query set.

No model, no data — purely exercises `validate_gold_select`. Each query is labelled
should_block (unsafe: DML/DDL/command/injection/out-of-scope/illegal-join/wildcard) or
not (safe). Reports block rate on unsafe queries and false-positive rate on safe ones.
This is the wrapper's core contribution and is exactly what Spider cannot measure.
Run inside the `api` image.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "services" / "api"))

from app.catalog import load_schema_catalog  # noqa: E402
from app.sql_guardrails import SQLValidationError, validate_gold_select  # noqa: E402

HUGE_LIMIT = 1_000_000_000


def is_blocked(sql: str, catalog) -> bool:
    try:
        validate_gold_select(sql, catalog, HUGE_LIMIT)
        return False
    except SQLValidationError:
        return True
    except Exception:  # noqa: BLE001 - a parse failure is also an effective block
        return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", default="contracts/semantic_catalog.yaml")
    parser.add_argument("--queries", default="benchmarks/safety/adversarial_queries.json")
    args = parser.parse_args()

    catalog = load_schema_catalog(Path(args.catalog))
    items = json.loads(Path(args.queries).read_text(encoding="utf-8"))

    unsafe = [q for q in items if q["should_block"]]
    safe = [q for q in items if not q["should_block"]]

    blocked_unsafe = 0
    leaked = []
    for q in unsafe:
        if is_blocked(q["sql"], catalog):
            blocked_unsafe += 1
        else:
            leaked.append(q)

    false_blocked = []
    for q in safe:
        if is_blocked(q["sql"], catalog):
            false_blocked.append(q)

    print("SAFETY (guardrail vs adversarial queries):")
    print(f"  unsafe blocked   = {blocked_unsafe}/{len(unsafe)} ({blocked_unsafe/len(unsafe):.1%})  <- block rate")
    print(f"  safe allowed     = {len(safe)-len(false_blocked)}/{len(safe)} ({(len(safe)-len(false_blocked))/len(safe):.1%})")
    print(f"  false positives  = {len(false_blocked)} (safe queries wrongly blocked)")

    by_cat = defaultdict(lambda: [0, 0])
    for q in unsafe:
        by_cat[q["category"]][1] += 1
        if is_blocked(q["sql"], catalog):
            by_cat[q["category"]][0] += 1
    print("\n  block rate by category:")
    for cat, (b, n) in sorted(by_cat.items()):
        print(f"    {cat:<20}: {b}/{n}")

    if leaked:
        print("\n  LEAKED (unsafe but allowed):")
        for q in leaked:
            print(f"    id={q['id']} [{q['category']}]: {q['sql'][:70]}")
    if false_blocked:
        print("\n  FALSE POSITIVES (safe but blocked):")
        for q in false_blocked:
            print(f"    id={q['id']}: {q['sql'][:70]}")


if __name__ == "__main__":
    main()
