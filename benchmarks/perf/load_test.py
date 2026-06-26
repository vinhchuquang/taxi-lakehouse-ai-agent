"""Concurrent load test for the lakehouse serving layer (req #3, real-world capacity).

Spawns N worker threads, each with its OWN read-only DuckDB connection, firing queries
from the taxi question pool back-to-back for a fixed duration. Sweeps concurrency levels
and reports sustained throughput (queries/sec) + latency p50/p95/p99 under load — the
evidence for "how many concurrent users the warehouse serves before it degrades".
Run inside the `api` service on the compose network (needs MinIO for zone tables).
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import random
import statistics
import sys
import threading
import time

import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "services" / "api"))

from app.query_engine import _configure_s3_access  # noqa: E402


def pct(values, p):
    if not values:
        return 0.0
    s = sorted(values)
    k = min(len(s) - 1, int(round((p / 100) * (len(s) - 1))))
    return s[k]


def _worker(db, queries, threads, deadline, out_lat, stop, think_ms):
    con = duckdb.connect(db, read_only=True)
    if threads:
        con.execute(f"SET threads={threads}")
    _configure_s3_access(con)
    lat, i = [], 0
    while time.perf_counter() < deadline and not stop.is_set():
        q = queries[i % len(queries)]
        i += 1
        t0 = time.perf_counter()
        con.execute(q).fetchall()
        lat.append((time.perf_counter() - t0) * 1000.0)
        if think_ms:  # human think time between queries (jittered 0.5x–1.5x)
            time.sleep(random.uniform(0.5, 1.5) * think_ms / 1000.0)
    con.close()
    out_lat.extend(lat)


def run_level(db, queries, concurrency, duration, threads, think_ms=0):
    buckets = [[] for _ in range(concurrency)]
    stop = threading.Event()
    start = time.perf_counter()
    deadline = start + duration
    ths = [threading.Thread(target=_worker,
                            args=(db, queries, threads, deadline, buckets[c], stop, think_ms))
           for c in range(concurrency)]
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    elapsed = time.perf_counter() - start
    lat = [x for b in buckets for x in b]
    n = len(lat)
    return {"concurrency": concurrency, "queries": n, "elapsed_s": round(elapsed, 2),
            "throughput_qps": round(n / elapsed, 1) if elapsed else 0.0,
            "p50_ms": round(pct(lat, 50), 1), "p95_ms": round(pct(lat, 95), 1),
            "p99_ms": round(pct(lat, 99), 1),
            "mean_ms": round(statistics.mean(lat), 1) if lat else 0.0}


def main():
    assert pct([1, 2, 3, 4], 100) == 4 and pct([5], 50) == 5, "pct broken"
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", default="/work/warehouse/analytics.duckdb")
    parser.add_argument("--questions", default="benchmarks/taxi/taxi_questions.json")
    parser.add_argument("--levels", default="1,2,4,8,16")
    parser.add_argument("--ids", default="", help="comma-separated question ids to include (default all)")
    parser.add_argument("--duration", type=float, default=20.0)
    parser.add_argument("--threads", type=int, default=0,
                        help="DuckDB threads per connection; 0 = default (all cores)")
    parser.add_argument("--think-ms", type=int, default=0,
                        help="human think time between queries per user, ms (jittered 0.5x-1.5x); 0 = hammer")
    parser.add_argument("--out", default="benchmarks/perf/load_results.json")
    args = parser.parse_args()

    items = json.loads(Path(args.questions).read_text(encoding="utf-8"))
    if args.ids:
        keep = {int(x) for x in args.ids.split(",")}
        items = [it for it in items if it["id"] in keep]
    queries = [it["query"] for it in items]
    threads = args.threads or None
    levels = [int(x) for x in args.levels.split(",")]

    warm = duckdb.connect(args.db, read_only=True)
    if threads:
        warm.execute(f"SET threads={threads}")
    _configure_s3_access(warm)
    for q in queries:
        warm.execute(q).fetchall()
    warm.close()

    cores = os.cpu_count()
    label = "users" if args.think_ms else "C"
    print(f"LAKEHOUSE LOAD TEST (cores={cores}, {args.duration:.0f}s/level, "
          f"threads/conn={threads or 'all'}, think={args.think_ms}ms, pool={len(queries)} queries):")
    rows = []
    for c in levels:
        row = run_level(args.db, queries, c, args.duration, threads, args.think_ms)
        rows.append(row)
        print(f"  {label}={c:<4} qps={row['throughput_qps']:<7} p50={row['p50_ms']:<8}"
              f"p95={row['p95_ms']:<9} p99={row['p99_ms']:<9} n={row['queries']}")

    Path(args.out).write_text(json.dumps(
        {"cores": cores, "duration_s": args.duration, "threads_per_conn": threads,
         "think_ms": args.think_ms, "levels": rows},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
