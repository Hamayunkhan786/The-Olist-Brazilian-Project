-- Exploratory Analysis: Top Customers by Order Value
-- Purpose: Identify high-value customers for business intelligence
-- Note: Analyses are not part of the dbt DAG, use for ad-hoc queries

SELECT 
    c.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,
    COUNT(DISTINCT f.order_id) as total_orders,
    SUM(f.total_order_amount) as total_spent,
    AVG(f.total_order_amount) as avg_order_value,
    MAX(f.purchase_at) as last_order_date
FROM {{ ref('dim_customers') }} c
LEFT JOIN {{ ref('fct_orders') }} f ON c.customer_id = f.customer_id
GROUP BY c.customer_id, c.customer_unique_id, c.customer_city, c.customer_state
ORDER BY total_spent DESC
LIMIT 100
