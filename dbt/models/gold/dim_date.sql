select
    pickup_date,
    extract(year from pickup_date) as year,
    extract(quarter from pickup_date) as quarter,
    extract(month from pickup_date) as month,
    extract(day from pickup_date) as day,
    dayname(pickup_date) as day_name,
    extract(dayofweek from pickup_date) as day_of_week,
    cast(strftime(pickup_date, '%Y-%m') as varchar) as year_month
from (
    select distinct pickup_date
    from {{ ref('silver_trips_unified') }}
    where pickup_date is not null
)
