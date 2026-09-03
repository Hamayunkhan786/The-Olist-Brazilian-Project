{{ config(materialized='table') }}

WITH payments AS (

    SELECT
        order_id,
        payment_sequential,
        payment_type,
        payment_installments,
        payment_value

    FROM {{ ref('stg_payments') }}

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
    p.order_id || '-' || p.payment_sequential AS payment_key,
    p.order_id,
    c.customer_unique_id AS customer_key,
    p.payment_sequential,
    p.payment_type,
    p.payment_installments,
    p.payment_value

FROM payments p
INNER JOIN orders o
    ON p.order_id = o.order_id
INNER JOIN customers c
    ON o.customer_id = c.customer_id