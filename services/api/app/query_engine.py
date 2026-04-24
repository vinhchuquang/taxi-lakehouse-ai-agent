from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

import duckdb


class QueryExecutionError(RuntimeError):
    pass


def execute_readonly_query(sql: str, duckdb_path: str) -> tuple[list[str], list[dict[str, Any]], int]:
    started_at = time.perf_counter()
    path = Path(duckdb_path)
    if not path.exists():
        raise QueryExecutionError(f"DuckDB database does not exist: {duckdb_path}")

    try:
        with duckdb.connect(str(path), read_only=True) as connection:
            _configure_s3_access(connection)
            cursor = connection.execute(sql)
            columns = [column[0] for column in cursor.description or []]
            rows = [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]
    except duckdb.Error as exc:
        raise QueryExecutionError(str(exc)) from exc

    execution_ms = int((time.perf_counter() - started_at) * 1000)
    return columns, rows, execution_ms


def _configure_s3_access(connection: duckdb.DuckDBPyConnection) -> None:
    endpoint = os.getenv("DUCKDB_S3_ENDPOINT") or _endpoint_from_minio_url(
        os.getenv("MINIO_ENDPOINT", "")
    )
    if not endpoint:
        return

    access_key = os.getenv("MINIO_ROOT_USER", "minioadmin")
    secret_key = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")
    region = os.getenv("DUCKDB_S3_REGION", "us-east-1")
    url_style = os.getenv("DUCKDB_S3_URL_STYLE", "path")
    use_ssl = os.getenv("DUCKDB_S3_USE_SSL", "false").lower()
    use_ssl_sql = "true" if use_ssl in {"1", "true", "yes"} else "false"

    if not _load_httpfs(connection):
        return

    connection.execute(f"set s3_endpoint = '{_sql_string(endpoint)}'")
    connection.execute(f"set s3_access_key_id = '{_sql_string(access_key)}'")
    connection.execute(f"set s3_secret_access_key = '{_sql_string(secret_key)}'")
    connection.execute(f"set s3_region = '{_sql_string(region)}'")
    connection.execute(f"set s3_url_style = '{_sql_string(url_style)}'")
    connection.execute(f"set s3_use_ssl = {use_ssl_sql}")


def _load_httpfs(connection: duckdb.DuckDBPyConnection) -> bool:
    try:
        connection.execute("load httpfs")
        return True
    except duckdb.Error:
        try:
            connection.execute("install httpfs")
            connection.execute("load httpfs")
            return True
        except duckdb.Error:
            return False


def _sql_string(value: str) -> str:
    return value.replace("'", "''")


def _endpoint_from_minio_url(value: str) -> str:
    return value.removeprefix("http://").removeprefix("https://").rstrip("/")
