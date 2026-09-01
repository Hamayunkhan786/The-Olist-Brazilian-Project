WITH raw_orders AS (
    SELECT 
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp,
        order_delivered_customer_date
    FROM {{ source('olist_raw', 'orders') }}  -- Yahan bhi 'olist_raw'
)

SELECT 
    order_id,
    customer_id,
    order_status,
    CAST(order_purchase_timestamp AS TIMESTAMP) AS purchase_at,
    CAST(order_delivered_customer_date AS TIMESTAMP) AS delivered_at
FROM raw_orders