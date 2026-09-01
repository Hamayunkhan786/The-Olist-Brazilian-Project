{% snapshot snap_orders %}

{{
    config(
      target_schema='marts',
      unique_key='order_id',
      strategy='check',
      check_cols=['order_status', 'order_approved_at', 'order_delivered_customer_date']
    )
}}

select * from {{ source('olist_raw', 'orders') }}

{% endsnapshot %}
