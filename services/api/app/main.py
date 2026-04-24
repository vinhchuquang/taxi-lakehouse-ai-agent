from fastapi import FastAPI, HTTPException

from app.agent import run_query_agent
from app.catalog import load_schema_catalog
from app.config import get_settings
from app.models import HealthResponse, QueryRequest, QueryResponse, SchemaResponse
from app.query_engine import QueryExecutionError
from app.sql_guardrails import SQLValidationError
from app.text_to_sql import SQLGenerationError

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
    settings = get_settings()
    catalog = load_schema_catalog(settings.semantic_catalog)

    try:
        return run_query_agent(
            request=request,
            catalog=catalog,
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            duckdb_path=settings.duckdb_path,
        )
    except SQLGenerationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except SQLValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except QueryExecutionError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
