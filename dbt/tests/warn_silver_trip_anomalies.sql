{{ config(severity = 'warn') }}

select
    service_type,
    pickup_at,
    dropoff_at,
    pickup_zone_id,
    dropoff_zone_id,
    trip_distance,
    fare_amount,
    total_amount
from {{ ref('silver_trips_unified') }}
where dropoff_at < pickup_at
   or trip_distance > 200
   or total_amount < 0
