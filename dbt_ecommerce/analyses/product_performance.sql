-- Exploratory Analysis: Product Performance
-- Purpose: Analyze product sales volume and revenue
-- Note: Analyses are not part of the dbt DAG, use for ad-hoc queries

SELECT 
    p.product_id,
    p.product_category_name,
    COUNT(DISTINCT oi.order_id) as total_orders,
    COUNT(oi.order_item_id) as total_items_sold,
    SUM(oi.price) as total_revenue,
    AVG(oi.price) as avg_price,
    MIN(oi.price) as min_price,
    MAX(oi.price) as max_price
FROM {{ ref('dim_products') }} p
LEFT JOIN {{ ref('stg_order_items') }} oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_category_name
ORDER BY total_revenue DESC
LIMIT 50
