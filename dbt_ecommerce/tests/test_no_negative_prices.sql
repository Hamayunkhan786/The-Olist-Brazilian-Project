-- Custom Test: No negative prices
-- Purpose: Ensure all prices are non-negative (data quality check)

{% test no_negative_prices(model, column_name) %}
    
    select *
    from {{ model }}
    where {{ column_name }} < 0
    
{% endtest %}
