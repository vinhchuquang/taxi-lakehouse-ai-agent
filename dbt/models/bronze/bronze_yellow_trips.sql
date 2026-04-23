select
    'yellow_taxi' as service_type,
    *
from read_parquet(
    '{{ var("yellow_tripdata_path", "s3://" ~ env_var("MINIO_BUCKET", "taxi-lakehouse") ~ "/bronze/yellow_taxi/**/*.parquet") }}',
    union_by_name = true
)
