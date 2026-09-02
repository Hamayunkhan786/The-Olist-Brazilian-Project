select order_id
from {{ ref('stg_orders') }}
where order_status not in ('canceled', 'unavailable')
    and order_id not in (
    select distinct order_id
    from {{ ref('stg_order_items') }}
)
