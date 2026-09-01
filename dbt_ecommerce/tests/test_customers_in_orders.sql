-- Custom Test: Ensure all customers have valid orders
-- Purpose: Check that dimension customers are used in fact tables

{% test customers_in_orders(model, column_name) %}
    
    select *
    from {{ model }}
    where {{ column_name }} is not null
    and {{ column_name }} not in (
        select distinct customer_id
        from {{ ref('fct_orders') }}
    )
    
{% endtest %}
