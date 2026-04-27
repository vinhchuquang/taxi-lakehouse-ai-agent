from __future__ import annotations

import argparse
import json
import statistics
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_API_URL = "http://localhost:8000/api/v1/query"
DEFAULT_OUTPUT = Path("docs/performance-benchmark-results.json")


@dataclass(frozen=True)
class BenchmarkCase:
    case_id: str
    name: str
    query_surface: str
    sql: str
    max_rows: int = 100


BENCHMARK_CASES = [
    BenchmarkCase(
        case_id="P01",
        name="Daily KPI trend",
        query_surface="aggregate mart: gold_daily_kpis",
        sql="""
            select service_type, pickup_date, trip_count, total_fare_amount, avg_trip_distance
            from gold_daily_kpis
            where pickup_date between date '2024-01-01' and date '2024-06-30'
            order by pickup_date, service_type
        """,
        max_rows=400,
    ),
    BenchmarkCase(
        case_id="P02",
        name="Zone demand ranking",
        query_surface="aggregate mart: gold_zone_demand",
        sql="""
            select zone_name, borough, sum(trip_count) as trips, sum(total_amount) as total_amount
            from gold_zone_demand
            where pickup_date between date '2024-01-01' and date '2024-06-30'
            group by zone_name, borough
            order by trips desc
        """,
        max_rows=25,
    ),
    BenchmarkCase(
        case_id="P03",
        name="Vendor aggregation",
        query_surface="star schema: fact_trips + dim_vendor",
        sql="""
            select v.vendor_name, count(*) as trips, sum(t.total_amount) as total_amount
            from fact_trips as t
            join dim_vendor as v on t.vendor_id = v.vendor_id
            where t.pickup_date between date '2024-01-01' and date '2024-06-30'
            group by v.vendor_name
            order by trips desc
        """,
        max_rows=20,
    ),
    BenchmarkCase(
        case_id="P04",
        name="Payment type aggregation",
        query_surface="star schema: fact_trips + dim_payment_type",
        sql="""
            select p.payment_type_name, count(*) as trips, sum(t.total_amount) as total_amount
            from fact_trips as t
            join dim_payment_type as p on t.payment_type = p.payment_type
            where t.pickup_date between date '2024-01-01' and date '2024-06-30'
            group by p.payment_type_name
            order by trips desc
        """,
        max_rows=20,
    ),
    BenchmarkCase(
        case_id="P05",
        name="Pickup/dropoff zone joins",
        query_surface="star schema: fact_trips + two dim_zone roles",
        sql="""
            select
                pickup_zone.borough as pickup_borough,
                dropoff_zone.borough as dropoff_borough,
                count(*) as trips
            from fact_trips as t
            join dim_zone as pickup_zone on t.pickup_zone_id = pickup_zone.zone_id
            join dim_zone as dropoff_zone on t.dropoff_zone_id = dropoff_zone.zone_id
            where t.pickup_date between date '2024-01-01' and date '2024-06-30'
            group by pickup_zone.borough, dropoff_zone.borough
            order by trips desc
        """,
        max_rows=50,
    ),
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Phase 17 API query performance benchmarks."
    )
    parser.add_argument("--api-url", default=DEFAULT_API_URL)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    if args.repeats < 1:
        raise SystemExit("--repeats must be at least 1")
    if args.warmup < 0:
        raise SystemExit("--warmup must be zero or greater")

    results = []
    for case in BENCHMARK_CASES:
        for _ in range(args.warmup):
            post_query(args.api_url, case)

        timings = []
        row_counts = []
        for _ in range(args.repeats):
            started = time.perf_counter()
            response = post_query(args.api_url, case)
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            timings.append(elapsed_ms)
            row_counts.append(len(response.get("rows", [])))

        results.append(
            {
                "case_id": case.case_id,
                "name": case.name,
                "query_surface": case.query_surface,
                "repeats": args.repeats,
                "row_count": row_counts[-1] if row_counts else 0,
                "min_ms": min(timings),
                "median_ms": int(statistics.median(timings)),
                "max_ms": max(timings),
                "samples_ms": timings,
            }
        )

    payload = {
        "benchmark": "phase17_api_query_performance",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "api_url": args.api_url,
        "warmup": args.warmup,
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print_markdown(results)
    print(f"\nWrote {args.output}")
    return 0


def post_query(api_url: str, case: BenchmarkCase) -> dict[str, Any]:
    body = json.dumps(
        {
            "question": case.name,
            "sql": " ".join(case.sql.split()),
            "max_rows": case.max_rows,
        }
    ).encode("utf-8")
    request = Request(
        api_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=300) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{case.case_id} failed with HTTP {exc.code}: {detail}") from exc
    except URLError as exc:
        raise RuntimeError(f"{case.case_id} failed to reach API: {exc.reason}") from exc


def print_markdown(results: list[dict[str, Any]]) -> None:
    print("| Case | Query | Surface | Rows | Median ms | Min ms | Max ms |")
    print("| --- | --- | --- | ---: | ---: | ---: | ---: |")
    for result in results:
        print(
            "| {case_id} | {name} | {query_surface} | {row_count} | "
            "{median_ms} | {min_ms} | {max_ms} |".format(**result)
        )


if __name__ == "__main__":
    raise SystemExit(main())
