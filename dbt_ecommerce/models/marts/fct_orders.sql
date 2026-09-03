{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

order_items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

order_item_aggregates AS (
    SELECT
        order_id,
        COUNT(order_item_id) AS total_items,
        SUM(price) AS total_order_amount,
        SUM(freight_value) AS total_freight_amount
    FROM order_items
    GROUP BY order_id
)

SELECT
    o.order_id,
    o.customer_id,
    o.order_status,
    o.purchase_at,
    o.delivered_at,
    COALESCE(a.total_items, 0) AS total_items,
    COALESCE(a.total_order_amount, 0.00) AS total_order_amount,
    COALESCE(a.total_freight_amount, 0.00) AS total_freight_amount,
    (COALESCE(a.total_order_amount, 0.00) + COALESCE(a.total_freight_amount, 0.00)) AS total_payment_value
FROM orders o
LEFT JOIN order_item_aggregates a
    ON o.order_id = a.order_id