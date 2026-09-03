{{ config(materialized='table') }}

WITH events AS (

    SELECT *
    FROM {{ ref('stg_customer_events') }}

),

customers AS (

    SELECT
        customer_id,
        customer_unique_id

    FROM {{ ref('stg_customers') }}

)

SELECT
    e.event_id AS event_key,
    e.event_id,
    c.customer_unique_id AS customer_key,
    e.customer_id,
    e.product_id,
    e.event_type,
    e.event_timestamp,
    e.device,
    e.session_id

FROM events e
LEFT JOIN customers c
    ON e.customer_id = c.customer_id