WITH raw_reviews AS (

    SELECT
        TRY_PARSE_JSON(RAW_DATA::VARCHAR):review_id::VARCHAR AS review_id,
        TRY_PARSE_JSON(RAW_DATA::VARCHAR):order_id::VARCHAR AS order_id,
        TRY_PARSE_JSON(RAW_DATA::VARCHAR):score::INTEGER AS review_score,
        TRY_TO_TIMESTAMP_NTZ(TRY_PARSE_JSON(RAW_DATA::VARCHAR):timestamps:creation_date::VARCHAR) AS review_created_date,
        TRY_TO_TIMESTAMP_NTZ(TRY_PARSE_JSON(RAW_DATA::VARCHAR):timestamps:answer_timestamp::VARCHAR) AS review_answered_date,
        TRY_PARSE_JSON(RAW_DATA::VARCHAR):comment:message::VARCHAR AS review_comment_message,
        TRY_PARSE_JSON(RAW_DATA::VARCHAR):comment:title::VARCHAR AS review_comment_title

    FROM {{ source('olist_raw', 'reviews') }}

)

SELECT
    review_id,
    order_id,
    review_score,
    review_created_date,
    review_answered_date,
    review_comment_message,
    review_comment_title

FROM raw_reviews