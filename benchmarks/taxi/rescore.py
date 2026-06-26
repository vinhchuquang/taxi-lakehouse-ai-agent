"""Re-score saved taxi_results.json offline (no Docker/API) using scoring.values_match.
Useful to re-evaluate after a scoring-logic change without re-querying the agent."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scoring import is_ordered, values_match  # noqa: E402


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "benchmarks/taxi/taxi_results.json"
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    flips = []
    n_match = 0
    for r in rows:
        if r.get("agent_error") or r.get("clarified"):
            continue
        ar, ac = r.get("agent_rows", []), r.get("agent_cols", [])
        gr, gc = r.get("gold_rows", []), r.get("gold_cols", [])
        ok = values_match(ar, ac, gr, gc, is_ordered(r["gold_sql"]))
        n_match += int(ok)
        if ok != bool(r.get("match")):
            flips.append((r["id"], r.get("match"), ok))
    print(f"offline re-score: {n_match}/{len(rows)} match ({n_match/len(rows):.1%})")
    if flips:
        print("flips (id, stored_match -> rescored):", flips)


if __name__ == "__main__":
    main()
