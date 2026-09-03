{{ config(materialized='table') }}

WITH calendar AS (

    SELECT
        DATEADD(
            day,
            SEQ4(),
            '2016-09-04'::DATE
        ) AS full_date

    FROM TABLE(
        GENERATOR(
            ROWCOUNT => 3580
        )
    )

)

SELECT
    TO_NUMBER(TO_CHAR(full_date, 'YYYYMMDD')) AS date_key,
    full_date,
    YEAR(full_date) AS year,
    QUARTER(full_date) AS quarter,
    QUARTER(full_date) AS quarter_number,
    MONTH(full_date) AS month,
    MONTH(full_date) AS month_number,
    MONTHNAME(full_date) AS month_name,
    TO_CHAR(full_date, 'YYYY-MM') AS month_year,
    WEEKOFYEAR(full_date) AS week_of_year,
    DAYOFMONTH(full_date) AS day_of_month,
    DAYOFWEEKISO(full_date) AS day_of_week,
    DAYNAME(full_date) AS day_name,
    DAYOFWEEKISO(full_date) IN (6, 7) AS is_weekend

FROM calendar