{% snapshot snap_customers %}

{{
    config(
      target_schema='marts',
      unique_key='customer_id',
      strategy='check',
      check_cols=['customer_city', 'customer_state']
    )
}}

select * from {{ source('olist_raw', 'customers') }}

{% endsnapshot %}