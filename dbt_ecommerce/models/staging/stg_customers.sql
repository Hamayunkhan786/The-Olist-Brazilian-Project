WITH raw_customers AS (
    SELECT 
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    FROM {{ source('olist_raw', 'customers') }}
)

SELECT 
    customer_id,
    customer_unique_id,
    CAST(customer_zip_code_prefix AS VARCHAR) AS zip_code,
    customer_city AS city,
    customer_state AS state
FROM raw_customers