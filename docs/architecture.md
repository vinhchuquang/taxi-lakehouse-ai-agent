# Architecture

## Goal

This project builds a local-first analytics platform on NYC TLC taxi data with a
read-only AI query interface.

## Main Components

- `Airflow` orchestrates monthly ingestion and downstream transforms.
- `MinIO` stores raw Bronze files as object storage.
- `dbt` models the transformation layers.
- `DuckDB` serves local analytics and query execution.
- `FastAPI` exposes schema and query endpoints to the AI layer.

## Data Flow

1. Download monthly TLC parquet files for `Yellow Taxi` and `Green Taxi`.
2. Download `Taxi Zone Lookup` as reference data.
3. Land raw files in `Bronze` and reference data in a stable local path.
4. Standardize both trip datasets into a shared `Silver` model and enrich with lookup data when needed.
5. Build curated marts in `Gold`.
6. Query `Gold` through BI tools and the AI agent.

The current architecture phase keeps Yellow and Green as the primary trip
datasets and only adds Taxi Zone Lookup as a supporting dimension source.

## Serving Principle

The AI layer must not query raw or partially cleaned data. It should only
operate over curated `Gold` tables and semantic metadata.

## Modeling Direction

Trong MVP, Gold đang ưu tiên curated aggregate marts như `gold_daily_kpis` và
`gold_zone_demand`. Cách này giúp dashboard và AI query trả lời các câu hỏi phổ
biến mà không phải tự join nhiều bảng.

Giai đoạn tiếp theo sẽ bổ sung dimensional layer trong Gold, gồm các model như
`dim_date`, `dim_zone`, `dim_service_type` và `fact_trips`. Các marts hiện tại
vẫn được giữ làm serving layer, sau đó có thể build lại từ `fact_trips` khi
dimensional layer ổn định.
