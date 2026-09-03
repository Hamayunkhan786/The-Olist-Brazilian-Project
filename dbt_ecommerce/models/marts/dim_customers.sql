{{ config(materialized='table') }}

select
    customer_unique_id as customer_key,
    customer_unique_id,
    min(customer_id) as customer_id,
    max(city) as customer_city,
    max(state) as customer_state

from {{ ref('stg_customers') }}
group by customer_unique_id