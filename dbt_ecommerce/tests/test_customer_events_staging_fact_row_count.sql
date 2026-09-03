SELECT 1 AS unexpected_result
FROM (
    SELECT COUNT(*) AS staging_count
    FROM {{ ref('stg_customer_events') }}
) s
JOIN (
    SELECT COUNT(*) AS fact_count
    FROM {{ ref('fct_customer_events') }}
) f ON TRUE
WHERE s.staging_count <> f.fact_count