from datetime import datetime
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
import types


def load_tlc_ingestion_module():
    module_path = Path("airflow/dags/lib/tlc_ingestion.py")
    spec = spec_from_file_location("tlc_ingestion", module_path)
    module = module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_build_tripdata_url_for_yellow() -> None:
    module = load_tlc_ingestion_module()
    url = module.build_tripdata_url("yellow", 2024, 1)

    assert url.endswith("/trip-data/yellow_tripdata_2024-01.parquet")


def test_build_trip_manifest_for_green() -> None:
    module = load_tlc_ingestion_module()
    manifest = module.build_trip_manifest("green", datetime(2024, 2, 1)).to_dict()

    assert manifest["service_type"] == "green_taxi"
    assert manifest["month"] == "02"
    assert manifest["local_relative_path"].endswith(
        "green_taxi/year=2024/month=02/green_tripdata_2024-02.parquet"
    )


def test_build_lookup_manifest() -> None:
    module = load_tlc_ingestion_module()
    manifest = module.build_lookup_manifest().to_dict()

    assert manifest["dataset"] == "taxi_zone_lookup"
    assert manifest["source_url"].endswith("/misc/taxi_zone_lookup.csv")
    assert manifest["local_relative_path"] == "reference/taxi_zone_lookup/taxi_zone_lookup.csv"


def test_upload_local_file_to_minio_creates_bucket_and_uploads(tmp_path) -> None:
    calls = []
    fake_boto3 = types.ModuleType("boto3")
    fake_botocore = types.ModuleType("botocore")
    fake_botocore_client = types.ModuleType("botocore.client")

    class FakeConfig:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    fake_botocore_client.Config = FakeConfig
    sys.modules["boto3"] = fake_boto3
    sys.modules["botocore"] = fake_botocore
    sys.modules["botocore.client"] = fake_botocore_client

    module = load_tlc_ingestion_module()
    local_file = tmp_path / "sample.parquet"
    local_file.write_bytes(b"sample")

    class FakeClient:
        def list_buckets(self):
            calls.append(("list_buckets",))
            return {"Buckets": []}

        def create_bucket(self, Bucket):
            calls.append(("create_bucket", Bucket))

        def upload_file(self, Filename, Bucket, Key):
            calls.append(("upload_file", Filename, Bucket, Key))

    def fake_client(*args, **kwargs):
        calls.append(("client", args, kwargs))
        return FakeClient()

    fake_boto3.client = fake_client

    result = module.upload_local_file_to_minio(
        manifest={
            "dataset": "yellow",
            "local_path": str(local_file),
            "bronze_object_key": "bronze/yellow_taxi/year=2024/month=01/sample.parquet",
        },
        minio_endpoint="http://minio:9000",
        minio_bucket="taxi-lakehouse",
        minio_access_key="minioadmin",
        minio_secret_key="minioadmin123",
    )

    assert ("create_bucket", "taxi-lakehouse") in calls
    assert (
        "upload_file",
        str(local_file),
        "taxi-lakehouse",
        "bronze/yellow_taxi/year=2024/month=01/sample.parquet",
    ) in calls
    assert result["minio_uri"] == (
        "s3://taxi-lakehouse/bronze/yellow_taxi/year=2024/month=01/sample.parquet"
    )
