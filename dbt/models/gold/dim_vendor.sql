select
    vendor_id,
    case vendor_id
        when '1' then 'Creative Mobile Technologies, LLC'
        when '2' then 'VeriFone Inc.'
        else 'Unknown vendor'
    end as vendor_name
from (
    select distinct vendor_id
    from {{ ref('silver_trips_unified') }}
    where vendor_id is not null
)
