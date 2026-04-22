{{ config(severity = 'error') }}

select
    'gold_daily_kpis is empty' as failure_reason
where not exists (
    select 1
    from {{ ref('gold_daily_kpis') }}
)
