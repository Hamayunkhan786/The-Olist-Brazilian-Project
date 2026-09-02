WITH raw_order_items AS (
    SELECT 
        order_id,
        order_item_id,
        product_id,
        seller_id,
        shipping_limit_date,
        price,
        freight_value
    FROM {{ source('olist_raw', 'order_items') }}
)

SELECT 
    order_id,
    order_item_id,
    product_id,
    seller_id,
    CAST(shipping_limit_date AS TIMESTAMP) AS shipping_limit_at,
    CAST(price AS NUMERIC(10, 2)) AS price,
    CAST(freight_value AS NUMERIC(10, 2)) AS freight_value
FROM raw_order_items