SELECT order_id

FROM {{ ref('fct_orders') }}

WHERE total_payment_value <> total_order_amount + total_freight_amount