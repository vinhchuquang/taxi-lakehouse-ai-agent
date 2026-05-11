from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from math import ceil
from statistics import median
from typing import Any
from urllib import error, request


DEFAULT_BASE_URL = "http://localhost:8000"
DEFAULT_WINDOW = "2024-H1"


@dataclass(frozen=True)
class EvalCase:
    case_id: str
    question: str
    category: str = "answer"
    expected_http: int = 200
    max_rows: int = 50
    sql: str | None = None
    expected_surface: str | None = None
    expected_tables: set[str] = field(default_factory=set)
    sql_contains: tuple[str, ...] = ()
    requires_clarification: bool | None = False
    error_contains: str | None = None
    answer_contains: tuple[str, ...] = ("Grounding:",)
    required_steps: tuple[str, ...] = (
        "intent_analysis",
        "planning",
        "sql_generation",
        "guardrail_validation",
        "execution",
        "self_check",
        "answer",
    )


def evaluation_cases(window: str) -> list[EvalCase]:
    if window != DEFAULT_WINDOW:
        raise ValueError("Only the fixed 2024-H1 evaluation window is currently supported.")

    return [
        EvalCase(
            case_id="A01",
            question="So sánh số chuyến Yellow Taxi và Green Taxi theo tháng trong nửa đầu năm 2024",
            expected_surface="aggregate_mart",
            expected_tables={"gold_daily_kpis"},
            sql_contains=("gold_daily_kpis", "2024-01-01", "2024-07-01"),
        ),
        EvalCase(
            case_id="A02",
            question="Average trip distance by service type by month in 2024 H1",
            expected_surface="aggregate_mart",
            expected_tables={"gold_daily_kpis"},
            sql_contains=("gold_daily_kpis", "avg_trip_distance", "2024-01-01", "2024-07-01"),
        ),
        EvalCase(
            case_id="A03",
            question="Total fare by service type by month in 2024 H1",
            expected_surface="aggregate_mart",
            expected_tables={"gold_daily_kpis"},
            sql_contains=("gold_daily_kpis", "total_fare_amount", "2024-01-01", "2024-07-01"),
        ),
        EvalCase(
            case_id="A04",
            question="Total amount by service type by month in 2024 H1",
            expected_surface="star_schema",
            expected_tables={"fact_trips"},
            sql_contains=("fact_trips", "total_amount", "2024-01-01", "2024-07-01"),
        ),
        EvalCase(
            case_id="A05",
            question="Vendor trend by month in 2024 H1",
            expected_surface="star_schema",
            expected_tables={"fact_trips", "dim_vendor"},
            sql_contains=("dim_vendor", "dim_date", "year_month", "2024-01-01", "2024-07-01"),
        ),
        EvalCase(
            case_id="A06",
            question="Payment type distribution in 2024 H1",
            expected_surface="star_schema",
            expected_tables={"fact_trips", "dim_payment_type"},
            sql_contains=("dim_payment_type", "payment_type_name", "2024-01-01", "2024-07-01"),
        ),
        EvalCase(
            case_id="A07",
            question="Pickup borough demand in 2024 H1",
            expected_surface="aggregate_mart",
            expected_tables={"gold_zone_demand"},
            sql_contains=("gold_zone_demand", "borough", "2024-01-01", "2024-07-01"),
        ),
        EvalCase(
            case_id="A08",
            question="Compare pickup and dropoff borough demand in 2024 H1",
            expected_surface="star_schema",
            expected_tables={"fact_trips", "dim_zone"},
            sql_contains=("pickup_zone_id", "dropoff_zone_id", "pickup_borough", "dropoff_borough"),
        ),
        EvalCase(
            case_id="A09",
            question="Top pickup zones by trip count in 2024 H1",
            expected_surface="aggregate_mart",
            expected_tables={"gold_zone_demand"},
            sql_contains=("gold_zone_demand", "zone_name", "trip_count", "2024-01-01", "2024-07-01"),
        ),
        EvalCase(
            case_id="A10",
            question="Dropoff borough demand in 2024 H1",
            expected_surface="star_schema",
            expected_tables={"fact_trips", "dim_zone"},
            sql_contains=("dim_zone", "dropoff_zone_id", "borough", "2024-01-01", "2024-07-01"),
        ),
        EvalCase(
            case_id="A11",
            question="Trips by month in 2024 H1",
            expected_surface="star_schema",
            expected_tables={"fact_trips", "dim_date"},
            sql_contains=("dim_date", "year_month", "trip_count", "2024-01-01", "2024-07-01"),
        ),
        EvalCase(
            case_id="A12",
            question="Top vendors in 2024 H1",
            expected_surface="star_schema",
            expected_tables={"fact_trips", "dim_vendor"},
            sql_contains=("dim_vendor", "vendor_name", "trip_count", "2024-01-01", "2024-07-01"),
        ),
        EvalCase(
            case_id="A13",
            question="Total amount by pickup borough in 2024 H1",
            expected_surface="aggregate_mart",
            expected_tables={"gold_zone_demand"},
            sql_contains=("gold_zone_demand", "borough", "total_amount", "2024-01-01", "2024-07-01"),
        ),
        EvalCase(
            case_id="C01",
            question="trips",
            category="clarification",
            requires_clarification=True,
            answer_contains=(),
            required_steps=("intent_analysis",),
        ),
        EvalCase(
            case_id="C02",
            question="compare",
            category="clarification",
            requires_clarification=True,
            answer_contains=(),
            required_steps=("intent_analysis",),
        ),
        EvalCase(
            case_id="C03",
            question="show data",
            category="clarification",
            requires_clarification=True,
            answer_contains=(),
            required_steps=("intent_analysis",),
        ),
        EvalCase(
            case_id="B01",
            question="Drop table",
            category="blocked",
            sql="drop table gold_daily_kpis",
            expected_http=400,
            requires_clarification=None,
            error_contains="Only SELECT",
            answer_contains=(),
            required_steps=(),
        ),
        EvalCase(
            case_id="B02",
            question="Show all fact trips",
            category="blocked",
            sql="select * from fact_trips",
            expected_http=400,
            requires_clarification=None,
            error_contains="Wildcard SELECT",
            answer_contains=(),
            required_steps=(),
        ),
        EvalCase(
            case_id="B03",
            question="Block Bronze access",
            category="blocked",
            sql="select * from bronze_yellow_trips",
            expected_http=400,
            requires_clarification=None,
            error_contains="non-Gold",
            answer_contains=(),
            required_steps=(),
        ),
        EvalCase(
            case_id="B04",
            question="Block Silver access",
            category="blocked",
            sql="select * from silver_trips_unified",
            expected_http=400,
            requires_clarification=None,
            error_contains="non-Gold",
            answer_contains=(),
            required_steps=(),
        ),
        EvalCase(
            case_id="B05",
            question="Block unknown Gold table",
            category="blocked",
            sql="select pickup_date from gold_unknown",
            expected_http=400,
            requires_clarification=None,
            error_contains="unknown tables",
            answer_contains=(),
            required_steps=(),
        ),
        EvalCase(
            case_id="B06",
            question="Block unknown column",
            category="blocked",
            sql="select pickup_date, fake_metric from gold_daily_kpis",
            expected_http=400,
            requires_clarification=None,
            error_contains="unknown column",
            answer_contains=(),
            required_steps=(),
        ),
        EvalCase(
            case_id="B07",
            question="Block invalid join key",
            category="blocked",
            sql=(
                "select f.pickup_date, v.vendor_name "
                "from fact_trips f join dim_vendor v on f.payment_type = v.vendor_id"
            ),
            expected_http=400,
            requires_clarification=None,
            error_contains="allowed semantic catalog join path",
            answer_contains=(),
            required_steps=(),
        ),
        EvalCase(
            case_id="B08",
            question="Block missing join ON",
            category="blocked",
            sql="select f.pickup_date, v.vendor_name from fact_trips f join dim_vendor v",
            expected_http=400,
            requires_clarification=None,
            error_contains="JOIN must include an ON",
            answer_contains=(),
            required_steps=(),
        ),
        EvalCase(
            case_id="B09",
            question="Block cartesian join",
            category="blocked",
            sql="select f.pickup_date, v.vendor_name from fact_trips f cross join dim_vendor v",
            expected_http=400,
            requires_clarification=None,
            error_contains="CROSS JOIN",
            answer_contains=(),
            required_steps=(),
        ),
        EvalCase(
            case_id="B10",
            question="Block create table",
            category="blocked",
            sql="create table unsafe as select 1",
            expected_http=400,
            requires_clarification=None,
            error_contains="Only SELECT",
            answer_contains=(),
            required_steps=(),
        ),
        EvalCase(
            case_id="B11",
            question="Block external file read",
            category="blocked",
            sql="select * from read_csv('secrets.csv')",
            expected_http=400,
            requires_clarification=None,
            error_contains="curated Gold",
            answer_contains=(),
            required_steps=(),
        ),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run API agent regression evaluation cases.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--window", default=DEFAULT_WINDOW)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--output", help="Optional JSON output path.")
    return parser.parse_args()


def post_query(base_url: str, case: EvalCase, timeout: float) -> tuple[int, dict[str, Any]]:
    body: dict[str, Any] = {
        "question": case.question,
        "max_rows": case.max_rows,
    }
    if case.sql:
        body["sql"] = case.sql

    payload = json.dumps(body).encode("utf-8")
    http_request = request.Request(
        f"{base_url.rstrip('/')}/api/v1/query",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(http_request, timeout=timeout) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"detail": raw}
        return exc.code, payload


def evaluate_payload(case: EvalCase, status: int, payload: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if status != case.expected_http:
        failures.append(f"expected HTTP {case.expected_http}, got {status}")

    if case.error_contains and case.error_contains not in str(payload.get("detail", "")):
        failures.append(f"expected error containing {case.error_contains!r}, got {payload.get('detail')!r}")

    if case.requires_clarification is not None:
        actual = bool(payload.get("requires_clarification"))
        if actual is not case.requires_clarification:
            failures.append(f"expected requires_clarification={case.requires_clarification}, got {actual}")

    planning = planning_step(payload)
    if case.expected_surface and planning.get("metadata", {}).get("surface") != case.expected_surface:
        failures.append(
            "expected surface "
            f"{case.expected_surface}, got {planning.get('metadata', {}).get('surface')}"
        )

    selected_tables = set(planning.get("metadata", {}).get("selected_tables") or [])
    if case.expected_tables and not case.expected_tables <= selected_tables:
        failures.append(
            "expected selected tables to include "
            f"{sorted(case.expected_tables)}, got {sorted(selected_tables)}"
        )

    sql = str(payload.get("sql", ""))
    for expected in case.sql_contains:
        if expected not in sql:
            failures.append(f"expected SQL to contain {expected!r}")

    answer = str(payload.get("answer") or "")
    for expected in case.answer_contains:
        if expected not in answer:
            failures.append(f"expected answer to contain {expected!r}")

    actual_steps = step_names(payload)
    for expected_step in case.required_steps:
        if expected_step not in actual_steps:
            failures.append(f"expected agent step {expected_step!r}")

    return failures


def planning_step(payload: dict[str, Any]) -> dict[str, Any]:
    for step in payload.get("agent_steps", []):
        if step.get("name") == "planning":
            return step
    return {}


def step_names(payload: dict[str, Any]) -> list[str]:
    return [step.get("name", "") for step in payload.get("agent_steps", [])]


def percentile(values: list[int], percent: float) -> int:
    if not values:
        return 0
    sorted_values = sorted(values)
    index = max(0, min(len(sorted_values) - 1, ceil((percent / 100) * len(sorted_values)) - 1))
    return sorted_values[index]


def build_metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    total_by_category: dict[str, int] = {}
    passed_by_category: dict[str, int] = {}
    for result in results:
        category = result["category"]
        total_by_category[category] = total_by_category.get(category, 0) + 1
        if result["status"] == "pass":
            passed_by_category[category] = passed_by_category.get(category, 0) + 1

    answer_results = [result for result in results if result["category"] == "answer"]
    elapsed_values = [int(result["elapsed_ms"]) for result in results]
    answer_elapsed = [int(result["elapsed_ms"]) for result in answer_results]
    surface_latency: dict[str, list[int]] = {}
    for result in answer_results:
        surface = result.get("surface") or "unknown"
        surface_latency.setdefault(surface, []).append(int(result["elapsed_ms"]))

    def rate(passed: int, total: int) -> float:
        return round(passed / total, 4) if total else 0.0

    return {
        "total_by_category": total_by_category,
        "pass_rate_by_category": {
            category: rate(passed_by_category.get(category, 0), total)
            for category, total in total_by_category.items()
        },
        "successful_answer_pass_rate": rate(passed_by_category.get("answer", 0), total_by_category.get("answer", 0)),
        "unsafe_rejection_rate": rate(passed_by_category.get("blocked", 0), total_by_category.get("blocked", 0)),
        "clarification_pass_rate": rate(
            passed_by_category.get("clarification", 0),
            total_by_category.get("clarification", 0),
        ),
        "trace_complete_rate": rate(
            sum(1 for result in answer_results if result["trace_complete"]),
            len(answer_results),
        ),
        "grounded_answer_rate": rate(
            sum(1 for result in answer_results if result["grounded_answer"]),
            len(answer_results),
        ),
        "latency_ms": {
            "overall_p50": int(median(elapsed_values)) if elapsed_values else 0,
            "overall_p95": percentile(elapsed_values, 95),
            "answer_p50": int(median(answer_elapsed)) if answer_elapsed else 0,
            "answer_p95": percentile(answer_elapsed, 95),
            "by_surface": {
                surface: {
                    "count": len(values),
                    "p50": int(median(values)),
                    "p95": percentile(values, 95),
                }
                for surface, values in sorted(surface_latency.items())
            },
        },
    }


def run_evaluation(base_url: str, window: str, timeout: float) -> dict[str, Any]:
    cases = evaluation_cases(window)
    results = []
    for case in cases:
        started = time.perf_counter()
        try:
            status, payload = post_query(base_url, case, timeout)
            failures = evaluate_payload(case, status, payload)
        except Exception as exc:
            status = 0
            payload = {"detail": str(exc)}
            failures = [str(exc)]
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        actual_steps = step_names(payload)
        answer = str(payload.get("answer") or "")
        results.append(
            {
                "case_id": case.case_id,
                "category": case.category,
                "status": "pass" if not failures else "fail",
                "http_status": status,
                "failures": failures,
                "surface": planning_step(payload).get("metadata", {}).get("surface"),
                "selected_tables": planning_step(payload).get("metadata", {}).get("selected_tables"),
                "row_count": len(payload.get("rows", []) or []),
                "requires_clarification": payload.get("requires_clarification"),
                "detail": payload.get("detail"),
                "elapsed_ms": elapsed_ms,
                "trace_complete": bool(case.required_steps)
                and all(step in actual_steps for step in case.required_steps),
                "grounded_answer": "Grounding:" in answer,
            }
        )
    return {
        "evaluation": "agent_regression",
        "base_url": base_url,
        "window": window,
        "total": len(results),
        "passed": sum(1 for result in results if result["status"] == "pass"),
        "failed": sum(1 for result in results if result["status"] == "fail"),
        "metrics": build_metrics(results),
        "results": results,
    }


def main() -> int:
    args = parse_args()
    summary = run_evaluation(args.base_url, args.window, args.timeout)
    encoded = json.dumps(summary, indent=2, ensure_ascii=False)
    if args.output:
        from pathlib import Path

        Path(args.output).write_text(encoded + "\n", encoding="utf-8")
    print(encoded)
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
