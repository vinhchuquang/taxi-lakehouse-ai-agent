select
    service_type,
    pickup_date,
    count(*) as trip_count,
    sum(fare_amount) as total_fare_amount,
    avg(trip_distance) as avg_trip_distance
from {{ ref('silver_trips_unified') }}
group by 1, 2
