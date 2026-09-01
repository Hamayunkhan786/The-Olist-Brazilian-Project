{# Macro: Log Processing Info #}
{# Purpose: Add debug logging to dbt models #}
{# Usage: {{ log_info("Processing orders table") }} #}

{% macro log_info(message) %}
    {% if execute %}
        {% do log(message, info=true) %}
    {% endif %}
{% endmacro %}


{# Macro: Row Count Assertion #}
{# Purpose: Assert that a model has expected row count #}
{# Usage: {{ assert_row_count(model_name, expected_count) }} #}

{% macro assert_row_count(model_name, expected_count) %}
    select case
        when row_count = 0 then 'ERROR: ' || '{{ model_name }}' || ' is empty!'
        when row_count < {{ expected_count }} then 'WARNING: ' || '{{ model_name }}' || ' has fewer rows than expected'
        else 'OK: ' || '{{ model_name }}' || ' has ' || cast(row_count as string) || ' rows'
    end as assertion_message
    from (select count(*) as row_count from {{ model_name }})
{% endmacro %}


{# Macro: Data Quality Check #}
{# Purpose: Check for NULL values in critical columns #}
{# Usage: {{ check_nulls('table_name', ['column1', 'column2']) }} #}

{% macro check_nulls(table_name, critical_columns) %}
    {% set cols = critical_columns|join(', ') %}
    select 
        {% for col in critical_columns %}
            sum(case when {{ col }} is null then 1 else 0 end) as {{ col }}_null_count
            {{ "," if not loop.last }}
        {% endfor %}
    from {{ table_name }}
{% endmacro %}
