select
    'green_taxi' as service_type,
    *
from read_parquet(
    '{{ var("green_tripdata_path", "s3://" ~ env_var("MINIO_BUCKET", "taxi-lakehouse") ~ "/bronze/green_taxi/**/*.parquet") }}',
    union_by_name = true
)
