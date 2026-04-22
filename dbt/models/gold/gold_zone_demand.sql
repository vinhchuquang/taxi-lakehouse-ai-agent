select
    t.service_type,
    t.pickup_date,
    z.zone_id,
    z.borough,
    z.zone_name,
    count(*) as trip_count,
    sum(t.total_amount) as total_amount
from {{ ref('fact_trips') }} as t
left join {{ ref('dim_zone') }} as z
    on t.pickup_zone_id = z.zone_id
group by 1, 2, 3, 4, 5
