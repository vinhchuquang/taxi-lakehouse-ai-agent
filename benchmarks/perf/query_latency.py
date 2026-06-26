"""Measure warehouse query latency for the lakehouse performance evaluation (req #3).

Opens one read-only DuckDB connection (with S3/MinIO config), warms the cache, then
times each taxi gold query `--runs` times. Reports median latency per query and the
overall p50/p95/mean, split by access path (aggregate mart vs star-schema/fact join) —
this is the evidence for "marts answer common questions faster than raw fact joins".
Run inside the `api` service on the compose network (needs MinIO for zone tables).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import statistics
import sys
import time

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "services" / "api"))

from app.query_engine import _configure_s3_access  # noqa: E402

MARTS = {"gold_daily_kpis", "gold_zone_demand"}


def access_path(tables) -> str:
    return "mart" if set(tables) <= MARTS else "star_schema"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="/work/warehouse/analytics.duckdb")
    parser.add_argument("--questions", default="benchmarks/taxi/taxi_questions.json")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--no-warmup", action="store_true",
                        help="skip warm-up: time the FIRST (cold) hit per query on a fresh connection")
    parser.add_argument("--out", default="benchmarks/perf/latency_results.json")
    args = parser.parse_args()

    items = json.loads(Path(args.questions).read_text(encoding="utf-8"))
    con = duckdb.connect(args.db, read_only=True)
    _configure_s3_access(con)

    results = []
    by_path = {"mart": [], "star_schema": []}
    for item in items:
        if not args.no_warmup:
            con.execute(item["query"]).fetchall()  # warm-up (cache)
        timings = []
        for _ in range(args.runs):
            t0 = time.perf_counter()
            con.execute(item["query"]).fetchall()
            timings.append((time.perf_counter() - t0) * 1000.0)
        med = statistics.median(timings)
        path = access_path(item.get("tables", []))
        by_path[path].append(med)
        results.append({"id": item["id"], "path": path, "median_ms": round(med, 1),
                        "min_ms": round(min(timings), 1), "difficulty": item["difficulty"]})
    con.close()

    Path(args.out).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    all_med = [r["median_ms"] for r in results]
    all_med.sort()

    def pct(values, p):
        if not values:
            return 0.0
        k = min(len(values) - 1, int(round((p / 100) * (len(values) - 1))))
        return sorted(values)[k]

    print(f"Wrote {args.out}\n")
    print(f"WAREHOUSE QUERY LATENCY ({args.runs} runs/query, {len(results)} queries):")
    print(f"  overall median_ms: p50={pct(all_med,50):.1f}  p95={pct(all_med,95):.1f}  mean={statistics.mean(all_med):.1f}")
    for path, vals in by_path.items():
        if vals:
            print(f"  {path:<12}: n={len(vals)}  median={statistics.median(vals):.1f}ms  max={max(vals):.1f}ms")


if __name__ == "__main__":
    main()
