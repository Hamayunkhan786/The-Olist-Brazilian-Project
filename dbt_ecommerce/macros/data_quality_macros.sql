{% macro log_info(message) %}
    {% if execute %}
        {% do log(message, info=true) %}
    {% endif %}
{% endmacro %}


{% macro assert_row_count(model_name, expected_count) %}
    select case
        when row_count = 0 then 'ERROR: ' || '{{ model_name }}' || ' is empty!'
        when row_count < {{ expected_count }} then 'WARNING: ' || '{{ model_name }}' || ' has fewer rows than expected'
        else 'OK: ' || '{{ model_name }}' || ' has ' || cast(row_count as string) || ' rows'
    end as assertion_message
    from (select count(*) as row_count from {{ model_name }})
{% endmacro %}


{% macro check_nulls(table_name, critical_columns) %}
    {% set cols = critical_columns|join(', ') %}
    select 
        {% for col in critical_columns %}
            sum(case when {{ col }} is null then 1 else 0 end) as {{ col }}_null_count
            {{ "," if not loop.last }}
        {% endfor %}
    from {{ table_name }}
{% endmacro %}
