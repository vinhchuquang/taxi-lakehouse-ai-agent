select
    'green_taxi' as service_type,
    *
from read_parquet(
    '{{ var("green_tripdata_path", "../data/bronze/green_taxi/**/*.parquet") }}',
    union_by_name = true
)
