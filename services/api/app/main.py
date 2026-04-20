from fastapi import FastAPI

from app.catalog import load_schema_catalog
from app.config import get_settings
from app.models import HealthResponse, QueryRequest, QueryResponse, SchemaResponse

app = FastAPI(
    title="Taxi Lakehouse AI Agent API",
    version="0.1.0",
    description="Basic API scaffold for the taxi lakehouse AI query service.",
)


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(
        status="ok",
        duckdb_path=settings.duckdb_path,
        semantic_catalog_loaded=settings.semantic_catalog.exists(),
    )


@app.get("/api/v1/schema", response_model=SchemaResponse)
def get_schema() -> SchemaResponse:
    settings = get_settings()
    return load_schema_catalog(settings.semantic_catalog)


@app.post("/api/v1/query", response_model=QueryResponse)
def query_data(request: QueryRequest) -> QueryResponse:
    sql = (
        "select pickup_date, trip_count, total_fare_amount "
        "from gold_daily_kpis limit {limit}"
    ).format(limit=request.max_rows)

    return QueryResponse(
        summary=(
            "This is a placeholder response. Replace it with schema retrieval, "
            "LLM SQL generation, validation, and DuckDB execution."
        ),
        sql=sql,
        columns=["pickup_date", "trip_count", "total_fare_amount"],
        rows=[],
        execution_ms=0,
    )
