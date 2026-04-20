# Runbook

## Local Setup

1. Review `.env`
2. Start services with `docker compose up --build`
3. Check:
   - Airflow at `http://localhost:8080`
   - MinIO Console at `http://localhost:9001`
   - API docs at `http://localhost:8000/docs`

## Expected Local Volumes

- `data/` for Bronze and local service data
- `logs/` for Airflow logs
- `warehouse/` for DuckDB database files

## Current Execution Notes

- Bronze ingestion currently starts with Yellow and Green monthly files.
- Keep the active ingestion scope limited to those two parquet sources.
- The next stable milestone is a runnable `Bronze -> Silver -> Gold` path on real TLC data.
- The AI API is scaffolded and not yet a full production query service.
