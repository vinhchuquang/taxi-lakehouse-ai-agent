select
    zone_id,
    borough,
    zone_name,
    service_zone
from {{ ref('bronze_taxi_zone_lookup') }}
