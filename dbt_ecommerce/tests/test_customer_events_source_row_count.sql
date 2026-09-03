WITH source_count AS (
    SELECT COUNT(*) AS row_count
    FROM {{ source('olist_raw', 'customer_events') }}
),

staging_count AS (
    SELECT COUNT(*) AS row_count
    FROM {{ ref('stg_customer_events') }}
)

SELECT 1 AS unexpected_result
FROM source_count s
JOIN staging_count t ON TRUE
WHERE s.row_count <> t.row_count