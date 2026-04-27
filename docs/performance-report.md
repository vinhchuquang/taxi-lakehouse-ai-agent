# Phase 17 Performance And Materialization Report

Verification date: `2026-04-27`

Status: completed for the current MVP. The benchmark harness is in place,
representative API timings were collected, and no dbt materialization change was
made because the measured latency is acceptable for the local thesis/demo
workflow.

## Scope

Phase 17 measures demo responsiveness for the fixed defense dataset window:

- `2024-01-01` through `2024-06-30`
- Yellow Taxi and Green Taxi
- Taxi Zone Lookup reference enrichment
- Gold aggregate marts and controlled Gold star-schema queries

The goal is to make materialization choices defensible. It is not to widen the
agent query surface or change SQL guardrails.

## Benchmark Harness

The repeatable benchmark command is:

```bash
python scripts/benchmark_phase17.py --repeats 5 --warmup 1
```

By default the script calls:

```text
http://localhost:8000/api/v1/query
```

It writes JSON results to:

```text
docs/performance-benchmark-results.json
```

The benchmark cases are:

| Case | Query | Query surface |
| --- | --- | --- |
| `P01` | Daily KPI trend | `gold_daily_kpis` aggregate mart |
| `P02` | Zone demand ranking | `gold_zone_demand` aggregate mart |
| `P03` | Vendor aggregation | `fact_trips` joined to `dim_vendor` |
| `P04` | Payment-type aggregation | `fact_trips` joined to `dim_payment_type` |
| `P05` | Pickup/dropoff zone joins | `fact_trips` joined to two `dim_zone` roles |

Each query filters to the Phase 12 defense window. Queries are submitted through
the API with SQL override, so the same read-only guardrails, max-row behavior,
DuckDB connection path, and audit logging path are exercised.

## Current Materialization Review

Current dbt materialization defaults:

| Layer | Current materialization |
| --- | --- |
| Silver | table |
| Gold | view |

Current Gold models:

| Model | Current role | Current materialization implication |
| --- | --- | --- |
| `fact_trips` | Trip-level Gold fact | View over `silver_trips_unified` |
| `dim_date` | Date dimension | View |
| `dim_zone` | Taxi Zone Lookup dimension | View over Bronze reference data |
| `dim_service_type` | Static service dimension | View |
| `dim_vendor` | Vendor dimension | View over Silver distinct vendor codes |
| `dim_payment_type` | Payment type dimension | View over Silver distinct payment codes |
| `gold_daily_kpis` | Common KPI fast path | View aggregating `fact_trips` |
| `gold_zone_demand` | Common zone-demand fast path | View joining `fact_trips` and `dim_zone` |

Because Gold is currently view-based, aggregate marts are semantically a fast
path for planning and guardrails, but they are not physically persisted as
precomputed DuckDB tables. That may be acceptable for the local dataset, but it
must be measured before changing dbt materialization.

## Decision

No materialization change was made.

Rationale:

- Aggregate mart benchmark medians were approximately `1.0` to `1.3` seconds
  through the full API/guardrail/audit path.
- Star-schema benchmark medians were approximately `1.1` to `4.1` seconds
  through the same path.
- Persisting `fact_trips` would duplicate a large trip-level table and increase
  local storage/build cost without evidence that the current demo needs it.
- Persisting only aggregate marts may improve the fastest paths, but current
  measured latency is already acceptable for the defense/demo flow.
- Keeping Gold as views preserves freshness after dbt rebuilds and keeps the
  local storage footprint lower.

## Benchmark Results

Command:

```bash
python scripts/benchmark_phase17.py --repeats 5 --warmup 1
```

Output file:

```text
docs/performance-benchmark-results.json
```

Results:

| Case | Query | Surface | Rows | Median ms | Min ms | Max ms |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `P01` | Daily KPI trend | `gold_daily_kpis` aggregate mart | `364` | `962` | `914` | `2999` |
| `P02` | Zone demand ranking | `gold_zone_demand` aggregate mart | `25` | `1265` | `1171` | `1415` |
| `P03` | Vendor aggregation | `fact_trips` plus `dim_vendor` | `3` | `3701` | `3348` | `4820` |
| `P04` | Payment-type aggregation | `fact_trips` plus `dim_payment_type` | `6` | `4062` | `3347` | `4416` |
| `P05` | Pickup/dropoff zone joins | `fact_trips` plus two `dim_zone` roles | `50` | `1078` | `1062` | `1256` |

Interpretation:

- The aggregate mart path remains the best default for common KPI and zone
  questions.
- Vendor and payment-type aggregations are slower because they scan the
  defense-window fact rows, but the latency is still acceptable for interactive
  thesis demos.
- The pickup/dropoff borough join is comparatively fast because the output
  cardinality is small and joins use small dimensions.
- The `P01` max sample includes one slower run, so future comparisons should use
  median timings rather than a single request.

## Verification

Runtime checks:

| Check | Result |
| --- | --- |
| `docker compose up -d` | Started existing stack without rebuild |
| `docker compose ps` | Postgres, MinIO, API, demo, Airflow scheduler, and Airflow webserver were running |
| `GET http://localhost:8000/healthz` | `status=ok`, `duckdb_exists=true`, `duckdb_connectable=true` |
| `GET http://localhost:8501` | HTTP `200` |
| `GET http://localhost:8080/health` | HTTP `200` |
| Phase 17 benchmark command | Completed and wrote `docs/performance-benchmark-results.json` |
| Valid API smoke query over `gold_daily_kpis` | Returned 5 rows |
| DDL guardrail smoke query | `drop table gold_daily_kpis` returned HTTP `400` |
| AST syntax parse for `scripts/benchmark_phase17.py` | Passed |
| `python -m pytest -p no:cacheprovider tests/test_semantic_catalog.py tests/test_sql_guardrails.py` | `5 passed, 1 skipped`; SQL guardrail tests remained dependency-gated on host |
| `python -m pytest -p no:cacheprovider` | `20 passed, 2 skipped`; API and SQL guardrail tests remained dependency-gated on host |

## Caveats

- Benchmarks measure end-to-end API calls, including SQL validation, DuckDB
  execution, response serialization, and audit logging. They are better demo
  timings than pure DuckDB operator timings.
- Host Python still does not have `duckdb`; Docker remains the preferred runtime
  verification path.
- SQL guardrail and API smoke tests remain dependency-gated in host pytest, so
  Docker HTTP smoke checks are recorded as runtime verification.
- If the thesis demo needs sub-second responses for every star-schema
  aggregation, revisit materialization with a before/after benchmark rather than
  changing dbt config speculatively.

## Future Materialization Option

If future measurements justify a change, the lowest-risk option is to
materialize only the two aggregate marts as tables while leaving `fact_trips` as
a view over the Silver table. That would preserve the flexible star-schema path
and avoid duplicating the largest table. Any such change should be followed by:

- dbt build inside the Airflow scheduler container
- before/after benchmark results using `scripts/benchmark_phase17.py`
- API smoke checks for aggregate marts, fact/dim joins, and blocked DDL
