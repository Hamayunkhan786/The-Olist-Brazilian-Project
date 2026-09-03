WITH raw_events AS (

    SELECT
        TRY_PARSE_JSON(RAW_DATA::VARCHAR) AS event_data

    FROM {{ source('olist_raw', 'customer_events') }}

)

SELECT
    event_data:event_id::VARCHAR AS event_id,
    event_data:customer_id::VARCHAR AS customer_id,
    event_data:product_id::VARCHAR AS product_id,
    event_data:event_type::VARCHAR AS event_type,
    TRY_TO_TIMESTAMP_NTZ(event_data:timestamp::VARCHAR) AS event_timestamp,
    event_data:device::VARCHAR AS device,
    event_data:session_id::VARCHAR AS session_id

FROM raw_events