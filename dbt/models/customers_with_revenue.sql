{{ config(
    materialized='table'
) }}

select
    user_id,
    count(id) as total_orders,
    sum(amount) as total_revenue
from {{ ref('raw_orders') }}
group by 1