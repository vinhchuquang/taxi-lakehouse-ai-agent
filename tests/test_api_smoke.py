from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

duckdb = pytest.importorskip("duckdb")
pytest.importorskip("httpx")

sys.path.insert(0, str(Path("services/api")))

from fastapi.testclient import TestClient  # noqa: E402


def build_test_client(tmp_path, monkeypatch) -> TestClient:
    catalog_path = tmp_path / "semantic_catalog.yaml"
    catalog_path.write_text(
        """
tables:
  - name: gold_daily_kpis
    description: Daily KPIs
    table_type: aggregate_mart
    execution_enabled: true
    grain: One row per service_type and pickup_date.
    fields:
      - name: service_type
        description: Taxi service type.
      - name: pickup_date
        description: Pickup date.
      - name: trip_count
        description: Trip count.
    dimensions:
      - service_type
      - pickup_date
    metrics:
      - name: trip_count
        description: Trip count.
    allowed_filters:
      - service_type
      - pickup_date
      - trip_count
    primary_key:
      - service_type
      - pickup_date
    foreign_keys: []
    allowed_joins: []
  - name: fact_trips
    description: Trip fact
    table_type: fact
    execution_enabled: true
    grain: One row per trip.
    fields:
      - name: pickup_date
        description: Pickup date.
      - name: vendor_id
        description: Vendor ID.
      - name: trip_distance
        description: Trip distance.
    dimensions:
      - pickup_date
      - vendor_id
    metrics:
      - name: trip_distance
        description: Trip distance.
    allowed_filters:
      - pickup_date
      - vendor_id
      - trip_distance
    primary_key: []
    foreign_keys: []
    allowed_joins:
      - left_table: fact_trips
        left_column: vendor_id
        right_table: dim_vendor
        right_column: vendor_id
  - name: dim_vendor
    description: Vendor dimension
    table_type: dimension
    execution_enabled: true
    grain: One row per vendor.
    fields:
      - name: vendor_id
        description: Vendor ID.
      - name: vendor_name
        description: Vendor name.
    dimensions:
      - vendor_id
      - vendor_name
    metrics: []
    allowed_filters:
      - vendor_id
      - vendor_name
    primary_key:
      - vendor_id
    foreign_keys: []
    allowed_joins: []
""".strip(),
        encoding="utf-8",
    )

    duckdb_path = tmp_path / "analytics.duckdb"
    with duckdb.connect(str(duckdb_path)) as connection:
        connection.execute(
            """
            create table gold_daily_kpis (
                service_type varchar,
                pickup_date date,
                trip_count integer
            )
            """
        )
        connection.execute(
            "insert into gold_daily_kpis values ('yellow_taxi', date '2024-01-01', 10)"
        )
        connection.execute(
            """
            create table fact_trips (
                pickup_date date,
                vendor_id integer,
                trip_distance double
            )
            """
        )
        connection.execute("insert into fact_trips values (date '2024-01-01', 1, 3.5)")
        connection.execute(
            """
            create table dim_vendor (
                vendor_id integer,
                vendor_name varchar
            )
            """
        )
        connection.execute("insert into dim_vendor values (1, 'Creative Mobile Technologies, LLC')")

    from app import main

    monkeypatch.setattr(
        main,
        "get_settings",
        lambda: SimpleNamespace(
            duckdb_path=str(duckdb_path),
            semantic_catalog=catalog_path,
            openai_api_key="replace-me",
            openai_model="gpt-4.1-mini",
        ),
    )
    return TestClient(main.app)


def test_query_endpoint_allows_gold_select_with_sql_override(tmp_path, monkeypatch) -> None:
    client = build_test_client(tmp_path, monkeypatch)

    response = client.post(
        "/api/v1/query",
        json={
            "question": "Show daily trips",
            "max_rows": 10,
            "sql": "select service_type, pickup_date, trip_count from gold_daily_kpis",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["columns"] == ["service_type", "pickup_date", "trip_count"]
    assert payload["rows"] == [
        {"service_type": "yellow_taxi", "pickup_date": "2024-01-01", "trip_count": 10}
    ]
    assert payload["sql"].endswith("LIMIT 10")
    assert payload["answer"]
    assert payload["confidence"] in {"high", "medium", "low"}
    assert [step["name"] for step in payload["agent_steps"]] == [
        "intent_analysis",
        "planning",
        "sql_generation",
        "guardrail_validation",
        "execution",
        "self_check",
        "answer",
    ]
    assert payload["agent_steps"][2]["status"] == "provided_sql"


def test_schema_endpoint_returns_full_catalog_metadata(tmp_path, monkeypatch) -> None:
    client = build_test_client(tmp_path, monkeypatch)

    response = client.get("/api/v1/schema")

    assert response.status_code == 200
    payload = response.json()
    assert {table["name"] for table in payload["tables"]} == {
        "gold_daily_kpis",
        "fact_trips",
        "dim_vendor",
    }
    mart = next(table for table in payload["tables"] if table["name"] == "gold_daily_kpis")
    fact = next(table for table in payload["tables"] if table["name"] == "fact_trips")
    vendor = next(table for table in payload["tables"] if table["name"] == "dim_vendor")
    assert mart["execution_enabled"] is True
    assert mart["primary_key"] == ["service_type", "pickup_date"]
    assert fact["execution_enabled"] is True
    assert len(fact["allowed_joins"]) == 1
    assert vendor["execution_enabled"] is True


def test_query_endpoint_rejects_non_gold_sql(tmp_path, monkeypatch) -> None:
    client = build_test_client(tmp_path, monkeypatch)

    response = client.post(
        "/api/v1/query",
        json={
            "question": "Show silver trips",
            "max_rows": 10,
            "sql": "select * from silver_trips_unified",
        },
    )

    assert response.status_code == 400
    assert "non-Gold" in response.json()["detail"]


def test_query_endpoint_allows_fact_dimension_join(tmp_path, monkeypatch) -> None:
    client = build_test_client(tmp_path, monkeypatch)

    response = client.post(
        "/api/v1/query",
        json={
            "question": "Show vendor trip distance",
            "max_rows": 10,
            "sql": (
                "select v.vendor_name, sum(f.trip_distance) as total_distance "
                "from fact_trips f "
                "join dim_vendor v on f.vendor_id = v.vendor_id "
                "group by v.vendor_name"
            ),
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["columns"] == ["vendor_name", "total_distance"]
    assert payload["rows"] == [
        {"vendor_name": "Creative Mobile Technologies, LLC", "total_distance": 3.5}
    ]


def test_query_endpoint_rejects_fact_wildcard_sql(tmp_path, monkeypatch) -> None:
    client = build_test_client(tmp_path, monkeypatch)

    response = client.post(
        "/api/v1/query",
        json={
            "question": "Show trip facts",
            "max_rows": 10,
            "sql": "select * from fact_trips",
        },
    )

    assert response.status_code == 400
    assert "Wildcard SELECT" in response.json()["detail"]


def test_query_endpoint_rejects_invalid_star_join(tmp_path, monkeypatch) -> None:
    client = build_test_client(tmp_path, monkeypatch)

    response = client.post(
        "/api/v1/query",
        json={
            "question": "Show bad star join",
            "max_rows": 10,
            "sql": (
                "select v.vendor_name, sum(f.trip_distance) as total_distance "
                "from fact_trips f "
                "join dim_vendor v on f.pickup_date = v.vendor_id "
                "group by v.vendor_name"
            ),
        },
    )

    assert response.status_code == 400
    assert "allowed semantic catalog join path" in response.json()["detail"]


def test_query_endpoint_rejects_ddl(tmp_path, monkeypatch) -> None:
    client = build_test_client(tmp_path, monkeypatch)

    response = client.post(
        "/api/v1/query",
        json={
            "question": "Drop a table",
            "max_rows": 10,
            "sql": "drop table gold_daily_kpis",
        },
    )

    assert response.status_code == 400
    assert "Only SELECT" in response.json()["detail"]


def test_query_endpoint_returns_clarification_for_ambiguous_question(tmp_path, monkeypatch) -> None:
    client = build_test_client(tmp_path, monkeypatch)

    response = client.post(
        "/api/v1/query",
        json={
            "question": "trips",
            "max_rows": 10,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["requires_clarification"] is True
    assert payload["clarification_question"]
    assert payload["rows"] == []
    assert payload["sql"] == ""
    assert payload["agent_steps"][0]["status"] == "needs_clarification"
