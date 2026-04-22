# Data Modeling Decisions

## Context

The project currently targets a local-first lakehouse for Yellow Taxi and Green
Taxi data. Taxi Zone Lookup is reference data for location enrichment.

Current flow:

1. `Bronze` keeps source data as raw as practical.
2. `Silver` normalizes Yellow and Green into one trip-level schema.
3. `Gold` serves BI, dashboards, and the read-only AI query API.

## Current Decision

The MVP keeps Gold as curated aggregate marts:

- `gold_daily_kpis`
- `gold_zone_demand`

This matches the current question patterns: daily KPIs, service type splits, and
zone-level demand. Aggregate marts keep the AI query surface small, reduce joins,
and make guardrails easier to reason about.

## Why Not Dim/Fact First

Dim/fact modeling is the right direction for a more mature warehouse, but it
adds early MVP complexity:

- More grain, key, and join-policy decisions.
- Higher risk of Text-to-SQL generating invalid or overly detailed joins.
- More guardrail complexity than a small set of curated Gold marts.
- No current need for many fact tables or reusable dimensions.

So the MVP proves ingestion, transforms, data quality, and safe AI querying
before adding a full dimensional layer.

## Next Direction

After the MVP is stable, add Gold dimensional models:

- `dim_date`
- `dim_zone`
- `dim_service_type`
- `fact_trips`

`fact_trips` should have one row per valid Silver trip. It should not replace
aggregate marts immediately. It should become the base for better marts and
drill-down analysis.

Keep `gold_daily_kpis` and `gold_zone_demand` as serving marts. Once the
dimensional layer is stable, rebuild these marts from `fact_trips` and the
related dimensions.

## AI Query Rules

- AI may query only Gold objects listed in the semantic catalog.
- Prefer aggregate marts for common questions.
- Expose `fact_trips` to AI only after cataloging its grain, metrics, and safe
  join paths.
- Never expose Bronze or Silver to AI.
- Never allow DML, DDL, or external file access.
