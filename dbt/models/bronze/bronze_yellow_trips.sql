select
    'yellow_taxi' as service_type,
    *
from read_parquet(
    '{{ var("yellow_tripdata_path", "../data/bronze/yellow_taxi/**/*.parquet") }}',
    union_by_name = true
)
