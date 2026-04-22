{{ config(severity = 'warn') }}

select
    service_type,
    pickup_date,
    trip_count,
    total_fare_amount,
    avg_trip_distance
from {{ ref('gold_daily_kpis') }}
where trip_count <= 0
   or total_fare_amount < 0
   or avg_trip_distance < 0
   or avg_trip_distance > 200
