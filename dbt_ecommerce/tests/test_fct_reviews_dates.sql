SELECT review_key

FROM {{ ref('fct_reviews') }}

WHERE review_answered_date < review_created_date