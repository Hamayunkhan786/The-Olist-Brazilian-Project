-- Custom Test: Ensure orders have valid order items
-- Purpose: Check data consistency between orders and order items

{% test orders_have_items(model, column_name) %}
    
    select *
    from {{ model }}
    where {{ column_name }} not in (
        select distinct order_id 
        from {{ ref('stg_order_items') }}
    )
    
{% endtest %}
