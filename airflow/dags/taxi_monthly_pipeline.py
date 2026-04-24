from __future__ import annotations

import logging
import os
from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator

from lib.dbt_runner import run_dbt_build
from lib.tlc_ingestion import (
    build_lookup_manifest,
    build_trip_manifest,
    ingest_file_to_minio,
    previous_month_starts,
)

LOCAL_DATA_ROOT = os.getenv("LOCAL_DATA_ROOT", "/opt/airflow/data")
TLC_DOWNLOAD_TIMEOUT_SECONDS = int(os.getenv("TLC_DOWNLOAD_TIMEOUT_SECONDS", "300"))
TLC_LOOKBACK_MONTHS = int(os.getenv("TLC_LOOKBACK_MONTHS", "3"))
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "taxi-lakehouse")
MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "minioadmin")
MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "minioadmin123")
LOGGER = logging.getLogger(__name__)


def resolve_run_dates(data_interval_start, dag_run=None) -> list[datetime]:
    if dag_run and dag_run.conf:
        year = dag_run.conf.get("year")
        month = dag_run.conf.get("month")
        if year and month:
            return [datetime(int(year), int(month), 1)]
    return previous_month_starts(data_interval_start, TLC_LOOKBACK_MONTHS)


with DAG(
    dag_id="taxi_monthly_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="0 0 15 * *",
    catchup=False,
    render_template_as_native_obj=True,
    tags=["taxi", "lakehouse", "elt", "yellow", "green"],
) as dag:
    start = EmptyOperator(task_id="start")

    @task
    def prepare_trip_manifests(data_interval_start=None, dag_run=None) -> list[dict[str, str]]:
        run_dates = resolve_run_dates(data_interval_start, dag_run)
        manifests = [
            build_trip_manifest(dataset, run_date).to_dict()
            for run_date in run_dates
            for dataset in ("yellow", "green")
        ]
        LOGGER.info("Prepared trip manifests: %s", manifests)
        return manifests

    @task
    def prepare_lookup_reference() -> dict[str, str]:
        manifest = build_lookup_manifest().to_dict()
        LOGGER.info("Prepared lookup manifest: %s", manifest)
        return manifest

    @task
    def ingest_to_bronze(manifest: dict[str, str]) -> dict[str, str]:
        LOGGER.info(
            "Starting Bronze ingestion for dataset=%s into root=%s and bucket=%s",
            manifest["dataset"],
            LOCAL_DATA_ROOT,
            MINIO_BUCKET,
        )
        result = ingest_file_to_minio(
            manifest=manifest,
            local_data_root=LOCAL_DATA_ROOT,
            minio_endpoint=MINIO_ENDPOINT,
            minio_bucket=MINIO_BUCKET,
            minio_access_key=MINIO_ROOT_USER,
            minio_secret_key=MINIO_ROOT_PASSWORD,
            timeout_seconds=TLC_DOWNLOAD_TIMEOUT_SECONDS,
        )
        LOGGER.info("Finished Bronze ingestion for dataset=%s: %s", manifest["dataset"], result)
        return result

    @task
    def build_silver_layer() -> None:
        LOGGER.info("Starting dbt build for Bronze and Silver layers")
        run_dbt_build("path:models/bronze path:models/silver")
        LOGGER.info("Completed dbt build for Bronze and Silver layers")

    @task
    def build_gold_layer() -> None:
        LOGGER.info("Starting dbt build for Gold layer")
        run_dbt_build("path:models/gold")
        LOGGER.info("Completed dbt build for Gold layer")

    publish_metadata = EmptyOperator(task_id="publish_metadata")
    done = EmptyOperator(task_id="done")

    trip_manifests = prepare_trip_manifests()
    lookup_manifest = prepare_lookup_reference()
    trip_bronze = ingest_to_bronze.override(task_id="ingest_trip_bronze").expand(
        manifest=trip_manifests
    )
    lookup_reference = ingest_to_bronze.override(task_id="ingest_taxi_zone_lookup")(lookup_manifest)
    build_silver = build_silver_layer()
    build_gold = build_gold_layer()

    start >> [trip_manifests, lookup_manifest]
    lookup_manifest >> lookup_reference
    trip_bronze >> build_silver
    lookup_reference >> build_silver
    build_silver >> build_gold >> publish_metadata >> done
