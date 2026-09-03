{{ config(materialized='table') }}

WITH reviews AS (

    SELECT *
    FROM {{ ref('stg_reviews') }}

),

orders AS (

    SELECT
        order_id,
        customer_id

    FROM {{ ref('stg_orders') }}

),

customers AS (

    SELECT
        customer_id,
        customer_unique_id

    FROM {{ ref('stg_customers') }}

)

SELECT
    r.review_id || '-' || r.order_id AS review_key,
    r.review_id,
    r.order_id,
    c.customer_unique_id AS customer_key,
    CASE
        WHEN o.order_id IS NOT NULL THEN 'MATCHED'
        ELSE 'UNMATCHED'
    END AS order_match_status,
    r.review_score,
    r.review_created_date,
    r.review_answered_date,
    r.review_comment_message,
    r.review_comment_title

FROM reviews r
LEFT JOIN orders o
    ON r.order_id = o.order_id
LEFT JOIN customers c
    ON o.customer_id = c.customer_id