select order_id, customer_id
from {{ ref('stg_orders') }}
where customer_id is not null
  and customer_id not in (
      select distinct customer_id
      from {{ ref('stg_customers') }}
  )
