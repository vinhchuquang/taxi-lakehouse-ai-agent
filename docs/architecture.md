# Architecture

## Goal

This project builds a local-first analytics platform on NYC TLC taxi data with a
read-only AI query interface.

## Main Components

- `Airflow` orchestrates monthly ingestion and downstream transforms.
- `MinIO` stores raw Bronze files as S3-compatible object storage.
- `dbt` models the transformation layers.
- `DuckDB` serves local analytics and query execution.
- `FastAPI` exposes schema and query endpoints to the AI layer.
- `Streamlit` provides a local demo UI.

## Data Flow

1. Airflow builds monthly manifests for Yellow Taxi, Green Taxi, and Taxi Zone
   Lookup.
2. Ingestion downloads each source file to local `data/` as a temporary cache.
3. Ingestion uploads the same file to MinIO under stable Bronze object keys.
4. dbt Bronze models read from MinIO `s3://taxi-lakehouse/...` paths using
   DuckDB `httpfs`.
5. dbt builds Silver normalized trip data and Gold star-schema models/marts in
   DuckDB.
6. FastAPI and Streamlit query curated Gold data through read-only DuckDB access.

## Storage Roles

- MinIO is the Bronze source of truth.
- Local `data/` is a download/cache location for ingestion and development
  fallback.
- DuckDB stores transformed Silver and Gold analytical tables in
  `warehouse/analytics.duckdb`.

## Modeling Direction

Gold contains both:

- a star schema: `fact_trips`, `dim_date`, `dim_zone`, `dim_service_type`,
  `dim_vendor`, and `dim_payment_type`
- aggregate marts: `gold_daily_kpis` and `gold_zone_demand`

Aggregate marts are the fast path for common dashboard and AI questions. The
star schema is the flexible analytical foundation and is exposed through
controlled API access after semantic metadata, column guardrails, wildcard
restrictions, and join guardrails validate generated SQL.

## Serving Principle

The AI layer must not query raw Bronze or partially cleaned Silver data. It
should operate over curated Gold tables and semantic metadata, with SQL validated
before execution. Fact/dimension queries must use explicit cataloged columns and
approved semantic join paths.

## Read-Only Agent Workflow

The query layer is a read-only AI query agent rather than a write-capable or
autonomous data agent. Its workflow is implemented directly in the FastAPI
service: intent analysis, query-surface planning, SQL generation, guardrail
validation, DuckDB execution, result self-checks, and answer synthesis. This
keeps the agent behavior visible for demos while preserving the project's
local-first, framework-light architecture.
