{{ config(severity = 'error') }}

select
    'gold_zone_demand is empty' as failure_reason
where not exists (
    select 1
    from {{ ref('gold_zone_demand') }}
)
