from __future__ import annotations

import logging
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from shutil import copyfileobj
from urllib.request import Request, urlopen

TLC_CLOUDFRONT_BASE_URL = "https://d37ci6vzurychx.cloudfront.net"
TRIP_DATASETS = {
    "yellow": "yellow_taxi",
    "green": "green_taxi",
}
DEFAULT_TIMEOUT_SECONDS = 300
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class TripDataManifest:
    dataset: str
    service_type: str
    year: str
    month: str
    source_url: str
    bronze_object_key: str
    local_relative_path: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ReferenceDataManifest:
    dataset: str
    service_type: str
    source_url: str
    bronze_object_key: str
    local_relative_path: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def build_tripdata_url(dataset: str, year: int, month: int) -> str:
    if dataset not in TRIP_DATASETS:
        raise ValueError(f"Unsupported dataset: {dataset}")

    return (
        f"{TLC_CLOUDFRONT_BASE_URL}/trip-data/"
        f"{dataset}_tripdata_{year:04d}-{month:02d}.parquet"
    )


def build_lookup_url() -> str:
    return f"{TLC_CLOUDFRONT_BASE_URL}/misc/taxi_zone_lookup.csv"


def month_start_with_lag(run_date: datetime, lag_months: int) -> datetime:
    if lag_months < 0:
        raise ValueError("lag_months must be non-negative")

    month_index = run_date.year * 12 + run_date.month - 1 - lag_months
    year = month_index // 12
    month = month_index % 12 + 1
    return datetime(year, month, 1)


def build_trip_manifest(dataset: str, run_date: datetime) -> TripDataManifest:
    if dataset not in TRIP_DATASETS:
        raise ValueError(f"Unsupported dataset: {dataset}")

    service_type = TRIP_DATASETS[dataset]
    year = run_date.year
    month = run_date.month
    file_name = f"{dataset}_tripdata_{year:04d}-{month:02d}.parquet"
    local_relative_path = (
        f"bronze/{service_type}/year={year:04d}/month={month:02d}/{file_name}"
    )

    return TripDataManifest(
        dataset=dataset,
        service_type=service_type,
        year=f"{year:04d}",
        month=f"{month:02d}",
        source_url=build_tripdata_url(dataset, year, month),
        bronze_object_key=local_relative_path,
        local_relative_path=local_relative_path,
    )


def build_lookup_manifest() -> ReferenceDataManifest:
    local_relative_path = "reference/taxi_zone_lookup/taxi_zone_lookup.csv"
    return ReferenceDataManifest(
        dataset="taxi_zone_lookup",
        service_type="reference_data",
        source_url=build_lookup_url(),
        bronze_object_key=local_relative_path,
        local_relative_path=local_relative_path,
    )


def resolve_local_path(local_data_root: str, local_relative_path: str) -> Path:
    return Path(local_data_root).joinpath(local_relative_path)


def compute_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe_local_file(path: Path) -> dict[str, str]:
    file_size_bytes = path.stat().st_size
    if file_size_bytes <= 0:
        raise ValueError(f"Downloaded file is empty: {path}")

    return {
        "local_path": str(path),
        "file_size_bytes": str(file_size_bytes),
        "sha256": compute_sha256(path),
    }


def download_file_to_local(
    manifest: dict[str, str],
    local_data_root: str,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, str]:
    destination_path = resolve_local_path(local_data_root, manifest["local_relative_path"])
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    LOGGER.info(
        "Downloading dataset=%s from %s to %s",
        manifest["dataset"],
        manifest["source_url"],
        destination_path,
    )

    request = Request(
        manifest["source_url"],
        headers={"User-Agent": "taxi-lakehouse-ai-agent/0.1"},
    )

    with urlopen(request, timeout=timeout_seconds) as response:
        with destination_path.open("wb") as destination_file:
            copyfileobj(response, destination_file)

    file_metadata = describe_local_file(destination_path)
    LOGGER.info(
        "Downloaded dataset=%s to %s (%s bytes, sha256=%s)",
        manifest["dataset"],
        destination_path,
        file_metadata["file_size_bytes"],
        file_metadata["sha256"],
    )

    return {
        **manifest,
        **file_metadata,
        "downloaded_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def upload_local_file_to_minio(
    manifest: dict[str, str],
    minio_endpoint: str,
    minio_bucket: str,
    minio_access_key: str,
    minio_secret_key: str,
) -> dict[str, str]:
    local_path = Path(manifest["local_path"])
    if not local_path.exists():
        raise FileNotFoundError(f"Local file does not exist: {local_path}")
    file_metadata = describe_local_file(local_path)

    import boto3
    from botocore.client import Config

    object_key = manifest["bronze_object_key"]
    client = boto3.client(
        "s3",
        endpoint_url=minio_endpoint,
        aws_access_key_id=minio_access_key,
        aws_secret_access_key=minio_secret_key,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )

    existing_buckets = {
        bucket["Name"]
        for bucket in client.list_buckets().get("Buckets", [])
    }
    if minio_bucket not in existing_buckets:
        LOGGER.info("Creating MinIO bucket=%s", minio_bucket)
        client.create_bucket(Bucket=minio_bucket)

    LOGGER.info(
        "Uploading dataset=%s from %s to s3://%s/%s",
        manifest["dataset"],
        local_path,
        minio_bucket,
        object_key,
    )
    client.upload_file(str(local_path), minio_bucket, object_key)
    LOGGER.info(
        "Uploaded dataset=%s to s3://%s/%s (%s bytes, sha256=%s)",
        manifest["dataset"],
        minio_bucket,
        object_key,
        file_metadata["file_size_bytes"],
        file_metadata["sha256"],
    )

    return {
        **manifest,
        **file_metadata,
        "minio_bucket": minio_bucket,
        "minio_endpoint": minio_endpoint,
        "minio_object_key": object_key,
        "minio_uri": f"s3://{minio_bucket}/{object_key}",
        "ingested_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def ingest_file_to_minio(
    manifest: dict[str, str],
    local_data_root: str,
    minio_endpoint: str,
    minio_bucket: str,
    minio_access_key: str,
    minio_secret_key: str,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, str]:
    downloaded_manifest = download_file_to_local(
        manifest=manifest,
        local_data_root=local_data_root,
        timeout_seconds=timeout_seconds,
    )
    return upload_local_file_to_minio(
        manifest=downloaded_manifest,
        minio_endpoint=minio_endpoint,
        minio_bucket=minio_bucket,
        minio_access_key=minio_access_key,
        minio_secret_key=minio_secret_key,
    )


def download_tripdata_to_local(
    manifest: dict[str, str],
    local_data_root: str,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> dict[str, str]:
    return download_file_to_local(
        manifest=manifest,
        local_data_root=local_data_root,
        timeout_seconds=timeout_seconds,
    )
