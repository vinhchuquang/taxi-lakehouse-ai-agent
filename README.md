# taxi-lakehouse-ai-agent

Taxi Lakehouse AI Agent is a graduation-project style repository for building a
local-first data lakehouse on taxi trip data and exposing a read-only AI query
agent over the curated analytics layer.

## Architecture

- `MinIO` stores raw and curated objects.
- `Airflow` orchestrates monthly ELT ingestion and transformation jobs.
- `dbt` models the `Bronze -> Silver -> Gold` layers.
- `DuckDB` serves the analytics layer consumed by BI and the AI agent.
- `FastAPI` exposes health, schema, and query endpoints for the AI query agent.

## Repository Layout

```text
.
|-- airflow/
|   `-- dags/
|-- dbt/
|   `-- models/
|-- services/
|   `-- api/
|-- contracts/
|-- infra/
|-- tests/
`-- docker-compose.yml
```

## Quick Start

1. Copy `.env.example` to `.env` and update secrets.
2. Review `docker-compose.yml`.
3. Start the local stack:

   ```bash
   docker compose up --build
   ```

4. Open:
   - Airflow: `http://localhost:8080`
   - MinIO Console: `http://localhost:9001`
   - API docs: `http://localhost:8000/docs`

## Initial Scope

- Ingest monthly `Yellow Taxi` and `Green Taxi` TLC trip data into `Bronze`
- Ingest `Taxi Zone Lookup` as the shared reference dataset
- Normalize and test data in `Silver`
- Publish curated marts in `Gold`
- Expose a read-only `Text-to-SQL` API over `Gold`

## TLC Data Sources

- Yellow Taxi trip parquet: monthly source files published by TLC
- Green Taxi trip parquet: monthly source files published by TLC
- Taxi Zone Lookup CSV: shared dimensional reference for pickup and dropoff zones

The pipeline intentionally starts with Yellow and Green only. `FHV` and
`HVFHV` stay out of scope until the core ELT flow is stable.

## Next Steps

- Replace the Bronze `EmptyOperator` tasks with download/upload operators
- Materialize Bronze parquet objects into DuckDB-accessible paths
- Add SQL validation and LLM integration in `services/api/app`
- Add integration tests once the first runnable pipeline is in place
