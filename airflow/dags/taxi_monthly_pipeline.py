from __future__ import annotations

from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator

TLC_CLOUDFRONT_BASE_URL = "https://d37ci6vzurychx.cloudfront.net"
TRIP_DATASETS = ("yellow", "green")


def build_tripdata_url(dataset: str, year: int, month: int) -> str:
    if dataset not in TRIP_DATASETS:
        raise ValueError(f"Unsupported dataset: {dataset}")
    return (
        f"{TLC_CLOUDFRONT_BASE_URL}/trip-data/"
        f"{dataset}_tripdata_{year:04d}-{month:02d}.parquet"
    )


def build_lookup_url() -> str:
    return f"{TLC_CLOUDFRONT_BASE_URL}/misc/taxi_zone_lookup.csv"


with DAG(
    dag_id="taxi_monthly_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@monthly",
    catchup=False,
    render_template_as_native_obj=True,
    tags=["taxi", "lakehouse", "elt", "yellow", "green"],
) as dag:
    start = EmptyOperator(task_id="start")
    build_context = EmptyOperator(task_id="build_context")

    @task
    def prepare_yellow_manifest(data_interval_start=None) -> dict[str, str]:
        year = data_interval_start.year
        month = data_interval_start.month
        return {
            "dataset": "yellow",
            "service_type": "yellow_taxi",
            "year": f"{year:04d}",
            "month": f"{month:02d}",
            "source_url": build_tripdata_url("yellow", year, month),
            "bronze_object_key": (
                f"bronze/yellow_taxi/year={year:04d}/month={month:02d}/"
                f"yellow_tripdata_{year:04d}-{month:02d}.parquet"
            ),
        }

    @task
    def prepare_green_manifest(data_interval_start=None) -> dict[str, str]:
        year = data_interval_start.year
        month = data_interval_start.month
        return {
            "dataset": "green",
            "service_type": "green_taxi",
            "year": f"{year:04d}",
            "month": f"{month:02d}",
            "source_url": build_tripdata_url("green", year, month),
            "bronze_object_key": (
                f"bronze/green_taxi/year={year:04d}/month={month:02d}/"
                f"green_tripdata_{year:04d}-{month:02d}.parquet"
            ),
        }

    @task
    def prepare_lookup_manifest() -> dict[str, str]:
        return {
            "dataset": "taxi_zone_lookup",
            "source_url": build_lookup_url(),
            "bronze_object_key": "reference/taxi_zone_lookup/taxi_zone_lookup.csv",
        }

    ingest_yellow_bronze = EmptyOperator(task_id="ingest_yellow_bronze")
    ingest_green_bronze = EmptyOperator(task_id="ingest_green_bronze")
    ingest_zone_lookup = EmptyOperator(task_id="ingest_zone_lookup")
    build_silver = EmptyOperator(task_id="build_silver")
    build_gold = EmptyOperator(task_id="build_gold")
    publish_metadata = EmptyOperator(task_id="publish_metadata")
    done = EmptyOperator(task_id="done")

    yellow_manifest = prepare_yellow_manifest()
    green_manifest = prepare_green_manifest()
    lookup_manifest = prepare_lookup_manifest()

    start >> build_context
    build_context >> yellow_manifest >> ingest_yellow_bronze
    build_context >> green_manifest >> ingest_green_bronze
    build_context >> lookup_manifest >> ingest_zone_lookup
    [ingest_yellow_bronze, ingest_green_bronze, ingest_zone_lookup] >> build_silver
    build_silver >> build_gold >> publish_metadata >> done
