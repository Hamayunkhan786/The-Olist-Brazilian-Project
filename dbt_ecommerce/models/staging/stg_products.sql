with source as (
    select * from {{ source('olist_raw', 'products') }}
),

renamed as (
    select
        TRY_PARSE_JSON(raw_data):product_id::varchar as product_id,
        TRY_PARSE_JSON(raw_data):product_category_name::varchar as product_category_name,
        TRY_TO_NUMBER(NULLIF(LOWER(TRIM(TRY_PARSE_JSON(raw_data):product_name_lenght::varchar)), 'nan')) as product_name_length,
        TRY_TO_NUMBER(NULLIF(LOWER(TRIM(TRY_PARSE_JSON(raw_data):product_description_lenght::varchar)), 'nan')) as product_description_length,
        TRY_TO_NUMBER(NULLIF(LOWER(TRIM(TRY_PARSE_JSON(raw_data):product_photos_qty::varchar)), 'nan')) as product_photos_qty,
        TRY_TO_NUMBER(NULLIF(LOWER(TRIM(TRY_PARSE_JSON(raw_data):product_weight_g::varchar)), 'nan')) as product_weight_g,
        TRY_TO_NUMBER(NULLIF(LOWER(TRIM(TRY_PARSE_JSON(raw_data):product_length_cm::varchar)), 'nan')) as product_length_cm,
        TRY_TO_NUMBER(NULLIF(LOWER(TRIM(TRY_PARSE_JSON(raw_data):product_height_cm::varchar)), 'nan')) as product_height_cm,
        TRY_TO_NUMBER(NULLIF(LOWER(TRIM(TRY_PARSE_JSON(raw_data):product_width_cm::varchar)), 'nan')) as product_width_cm,
        ingestion_timestamp
    from source
)

select * from renamed