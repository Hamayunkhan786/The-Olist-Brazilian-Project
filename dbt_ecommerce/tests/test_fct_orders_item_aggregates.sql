WITH expected AS (

    SELECT
        order_id,
        COUNT(order_item_id) AS total_items,
        SUM(price) AS total_order_amount,
        SUM(freight_value) AS total_freight_amount

    FROM {{ ref('stg_order_items') }}
    GROUP BY order_id

),

actual AS (

    SELECT
        order_id,
        total_items,
        total_order_amount,
        total_freight_amount

    FROM {{ ref('fct_orders') }}

)

SELECT
    a.order_id

FROM actual a
LEFT JOIN expected e
    ON a.order_id = e.order_id

WHERE a.total_items <> COALESCE(e.total_items, 0)
   OR a.total_order_amount <> COALESCE(e.total_order_amount, 0.00)
   OR a.total_freight_amount <> COALESCE(e.total_freight_amount, 0.00)