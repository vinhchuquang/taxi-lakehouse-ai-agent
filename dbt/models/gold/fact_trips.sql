select
    service_type,
    source_year,
    source_month,
    pickup_date,
    pickup_at,
    dropoff_at,
    vendor_id,
    pickup_zone_id,
    dropoff_zone_id,
    passenger_count,
    trip_distance,
    fare_amount,
    total_amount,
    payment_type
from {{ ref('silver_trips_unified') }}
