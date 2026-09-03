WITH raw_payments AS (

    SELECT
        order_id,
        payment_sequential,
        payment_type,
        payment_installments,
        payment_value

    FROM {{ source('olist_raw', 'order_payments') }}

)

SELECT
    order_id,
    payment_sequential,
    payment_type,
    CAST(payment_installments AS INTEGER) AS payment_installments,
    CAST(payment_value AS NUMERIC(10, 2)) AS payment_value

FROM raw_payments