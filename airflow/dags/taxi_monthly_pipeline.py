from __future__ import annotations

import os
from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator

from lib.tlc_ingestion import build_lookup_manifest, build_trip_manifest, download_file_to_local

LOCAL_DATA_ROOT = os.getenv("LOCAL_DATA_ROOT", "/opt/airflow/data")
TLC_DOWNLOAD_TIMEOUT_SECONDS = int(os.getenv("TLC_DOWNLOAD_TIMEOUT_SECONDS", "300"))


with DAG(
    dag_id="taxi_monthly_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@monthly",
    catchup=False,
    render_template_as_native_obj=True,
    tags=["taxi", "lakehouse", "elt", "yellow", "green"],
) as dag:
    start = EmptyOperator(task_id="start")

    @task
    def prepare_yellow_manifest(data_interval_start=None) -> dict[str, str]:
        return build_trip_manifest("yellow", data_interval_start).to_dict()

    @task
    def prepare_green_manifest(data_interval_start=None) -> dict[str, str]:
        return build_trip_manifest("green", data_interval_start).to_dict()

    @task
    def prepare_lookup_reference() -> dict[str, str]:
        return build_lookup_manifest().to_dict()

    @task
    def ingest_to_local(manifest: dict[str, str]) -> dict[str, str]:
        return download_file_to_local(
            manifest=manifest,
            local_data_root=LOCAL_DATA_ROOT,
            timeout_seconds=TLC_DOWNLOAD_TIMEOUT_SECONDS,
        )

    build_silver = EmptyOperator(task_id="build_silver")
    build_gold = EmptyOperator(task_id="build_gold")
    publish_metadata = EmptyOperator(task_id="publish_metadata")
    done = EmptyOperator(task_id="done")

    yellow_manifest = prepare_yellow_manifest()
    green_manifest = prepare_green_manifest()
    lookup_manifest = prepare_lookup_reference()
    yellow_bronze = ingest_to_local.override(task_id="ingest_yellow_bronze")(yellow_manifest)
    green_bronze = ingest_to_local.override(task_id="ingest_green_bronze")(green_manifest)
    lookup_reference = ingest_to_local.override(task_id="ingest_taxi_zone_lookup")(lookup_manifest)

    start >> [yellow_manifest, green_manifest, lookup_manifest]
    yellow_manifest >> yellow_bronze
    green_manifest >> green_bronze
    lookup_manifest >> lookup_reference
    [yellow_bronze, green_bronze, lookup_reference] >> build_silver
    build_silver >> build_gold >> publish_metadata >> done
