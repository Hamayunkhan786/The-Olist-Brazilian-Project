with source as (
    select * from {{ source('olist_raw', 'products') }}
),

renamed as (
    select
        -- JSON VARIANT field se product_id extract karna (Snowflake syntax)
        RAW_DATA:product_id::varchar as product_id,
        RAW_DATA:product_category_name::varchar as product_category_name,
        RAW_DATA:product_name_length::integer as product_name_length,
        RAW_DATA:product_description_length::integer as product_description_length,
        RAW_DATA:product_photos_qty::integer as product_photos_qty,
        RAW_DATA:product_weight_g::integer as product_weight_g,
        RAW_DATA:product_length_cm::integer as product_length_cm,
        RAW_DATA:product_height_cm::integer as product_height_cm,
        RAW_DATA:product_width_cm::integer as product_width_cm,
        ingestion_timestamp
    from source
)

select * from renamed