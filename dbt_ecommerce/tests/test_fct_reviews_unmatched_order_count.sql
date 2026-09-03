SELECT 1 AS unexpected_result

FROM {{ ref('fct_reviews') }}

GROUP BY TRUE

HAVING COUNT_IF(order_match_status = 'UNMATCHED') <> 1650