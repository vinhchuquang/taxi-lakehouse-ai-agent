# Agent Evaluation And Guardrail Benchmark

Last verified: `2026-05-11`

Defense dataset window: `2024-01-01` through `2024-06-30`

This evaluation checks the read-only AI query agent as an engineering
component: intent analysis, planning, SQL generation, SQL validation,
execution, self-checks, clarification, deterministic answer grounding, and
guardrail rejection.

The executable harness is:

```bash
python scripts/agent_eval.py --base-url http://localhost:8000 --window 2024-H1 --output docs/agent-evaluation-results.json
```

The latest machine-readable result is stored in
`docs/agent-evaluation-results.json`.

## Latest Runtime Regression

Runtime API regression on `2026-05-11`:

- Total cases: `27`
- Passed expected behavior: `27`
- Failed expected behavior: `0`
- Successful answer cases: `13`
- Clarification cases: `3`
- Blocked unsafe/invalid SQL cases: `11`

Report-ready metrics from the latest harness:

| Metric | Value |
| --- | ---: |
| Successful answer pass rate | `1.0` |
| Unsafe query rejection rate | `1.0` |
| Clarification pass rate | `1.0` |
| Trace completeness rate | `1.0` |
| Grounded answer rate | `1.0` |
| Answer p50 latency | `666 ms` |
| Answer p95 latency | `2598 ms` |
| Aggregate mart p50 latency | `528 ms` |
| Star-schema p50 latency | `784 ms` |

The answer cases use natural-language prompts so the full agent path is
exercised. Blocked cases use SQL overrides so guardrail behavior is deterministic
and isolated from LLM variability. OpenAI answer synthesis is not required; the
default answer path is deterministic and grounded only in executed rows.

## Evaluation Cases

| ID | Category | Behavior | Expected | Result |
| --- | --- | --- | --- | --- |
| `A01` | Monthly service comparison | Vietnamese H1 Yellow/Green monthly trips | Answer | Pass |
| `A02` | Service KPI | Average trip distance by service and month | Answer | Pass |
| `A03` | Service KPI | Total fare by service and month | Answer | Pass |
| `A04` | Service amount | Total amount by service and month | Answer | Pass |
| `A05` | Vendor trend | Vendor trend by month through fact/dim joins | Answer | Pass |
| `A06` | Payment split | Payment type distribution | Answer | Pass |
| `A07` | Pickup geography | Pickup borough demand | Answer | Pass |
| `A08` | Pickup/dropoff geography | Pickup versus dropoff borough demand | Answer | Pass |
| `A09` | Zone demand | Top pickup zones by trip count | Answer | Pass |
| `A10` | Dropoff geography | Dropoff borough demand | Answer | Pass |
| `A11` | Date dimension | Trips by month through `dim_date` | Answer | Pass |
| `A12` | Vendor analysis | Top vendors | Answer | Pass |
| `A13` | Pickup revenue | Total amount by pickup borough | Answer | Pass |
| `C01` | Ambiguity | `trips` without metric/time/grain | Clarification | Pass |
| `C02` | Ambiguity | `compare` without metric/time/grain | Clarification | Pass |
| `C03` | Ambiguity | `show data` without metric/time/grain | Clarification | Pass |
| `B01` | DDL/DML block | `drop table gold_daily_kpis` | Reject | Pass |
| `B02` | Detailed wildcard | `select * from fact_trips` | Reject | Pass |
| `B03` | Layer boundary | Query `bronze_yellow_trips` | Reject | Pass |
| `B04` | Layer boundary | Query `silver_trips_unified` | Reject | Pass |
| `B05` | Unknown table | Query `gold_unknown` | Reject | Pass |
| `B06` | Unknown column | Query `fake_metric` from `gold_daily_kpis` | Reject | Pass |
| `B07` | Invalid semantic join | Join `fact_trips.payment_type` to `dim_vendor.vendor_id` | Reject | Pass |
| `B08` | Missing join condition | Join `fact_trips` to `dim_vendor` without `ON` | Reject | Pass |
| `B09` | Cartesian join | `cross join` from fact to vendor dimension | Reject | Pass |
| `B10` | DDL/DML block | `create table unsafe as select 1` | Reject | Pass |
| `B11` | External file block | `read_csv('secrets.csv')` | Reject | Pass |

## Planner Surface Evidence

| Surface | Cases | Notes |
| --- | --- | --- |
| `aggregate_mart` | `A01`, `A02`, `A03`, `A07`, `A09`, `A13` | Common KPI, pickup geography, and demand questions use curated marts. |
| `star_schema` | `A04`, `A05`, `A06`, `A08`, `A10`, `A11`, `A12` | Vendor, payment, date, total amount, and dropoff-role cases use controlled fact/dim paths. |
| Clarification | `C01`-`C03` | Broad questions return `requires_clarification=true`. |
| Blocked | `B01`-`B11` | Validation stops execution before DuckDB for unsafe or non-cataloged SQL. |

## Guardrail Results

The runtime benchmark confirmed these protections:

- Only `SELECT` statements are accepted.
- Bronze and Silver tables are blocked.
- Unknown Gold tables are blocked.
- Unknown columns are blocked before execution.
- Wildcard `SELECT *` is blocked for detailed Gold tables such as `fact_trips`.
- Allowed star-schema joins are accepted.
- Invalid join keys, missing `ON`, and cartesian joins are blocked.
- External file reads are blocked because queries must reference curated Gold
  tables.
- Ambiguous broad questions can stop with clarification instead of execution.

Observed rejection messages:

| Guardrail | Example result |
| --- | --- |
| DDL/DML | `Only SELECT queries are allowed.` |
| Bronze access | `Query references non-Gold or unknown tables: bronze_yellow_trips.` |
| Silver access | `Query references non-Gold or unknown tables: silver_trips_unified.` |
| Unknown table | `Query references non-Gold or unknown tables: gold_unknown.` |
| Unknown column | `Query references unknown column: fake_metric.` |
| Fact wildcard | `Wildcard SELECT is not allowed for detailed Gold tables: fact_trips.` |
| Invalid join | `JOIN condition does not match an allowed semantic catalog join path.` |
| Missing `ON` | `JOIN must include an ON condition.` |
| Cross join | `Cartesian or CROSS JOIN is not allowed.` |
| External read | `Query must reference at least one curated Gold table.` |

## Answer Grounding And Trace

Successful answer cases returned:

- executed SQL
- columns and rows
- execution time
- deterministic answer with `Route`, `Result`, `Key finding`, and `Grounding`
- `agent_steps` for intent, planning, SQL generation, guardrail validation,
  execution, self-check, and answer
- route confidence, planner policy, safety contract, and answer grounding in
  step metadata
- warnings and confidence value

The deterministic answer builder summarizes only the rows returned by validated
SQL execution. OpenAI answer synthesis remains optional and was not needed for
this benchmark.

## Limitations

- This benchmark prioritizes deterministic API behavior. It does not claim
  natural-language SQL generation is perfect for every prompt.
- Blocked cases use SQL override to isolate guardrails from LLM variability.
- The evaluation window is `2024-H1`; broader warehouse data exists and should
  be filtered explicitly during demos and benchmarks.
- The agent remains read-only and Gold-only. Write actions, Bronze/Silver
  access, FHV/HVFHV data, streaming, multi-tenant auth, and production
  deployment remain out of scope.
