{{ config(materialized='table') }}

WITH order_items AS (

    SELECT
        order_id,
        order_item_id,
        product_id,
        seller_id,
        shipping_limit_at,
        price,
        freight_value

    FROM {{ ref('stg_order_items') }}

)

SELECT
    order_id || '-' || order_item_id AS order_item_key,
    order_id,
    order_item_id,
    product_id,
    seller_id,
    shipping_limit_at,
    price,
    freight_value,
    1 AS quantity

FROM order_items