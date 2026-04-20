# Architecture

## Goal

This project builds a local-first analytics platform on NYC TLC taxi data with a
read-only AI query interface.

## Main Components

- `Airflow` orchestrates monthly ingestion and downstream transforms.
- `MinIO` stores raw and curated files as object storage.
- `dbt` models the transformation layers.
- `DuckDB` serves local analytics and query execution.
- `FastAPI` exposes schema and query endpoints to the AI layer.

## Data Flow

1. Download monthly TLC parquet files for `Yellow Taxi` and `Green Taxi`.
2. Land raw files in `Bronze`.
3. Standardize both datasets into a shared `Silver` model.
4. Build curated marts in `Gold`.
5. Query `Gold` through BI tools and the AI agent.

The current architecture phase intentionally focuses only on these two trip
datasets and does not expand to additional TLC sources unless explicitly
requested.

## Serving Principle

The AI layer must not query raw or partially cleaned data. It should only
operate over curated `Gold` tables and semantic metadata.
