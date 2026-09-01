{% macro generate_surrogate_key(column_names) %}
    {% if execute %}
        {% set col_str = ', '.join(column_names) %}
    {% else %}
        {% set col_str = '' %}
    {% endif %}
    md5(cast(concat({{ col_str }}) as string))
{% endmacro %}


{% macro format_timestamp(column) %}
    to_timestamp_ntz({{ column }})
{% endmacro %}


{% macro generate_date_spine(start_date, end_date) %}
    with date_spine as (
        select 
            dateadd(day, seq4(), '{{ start_date }}'::date) as date_day
        from table(generator(rowcount => (datediff(day, '{{ start_date }}'::date, '{{ end_date }}'::date) + 1)))
        where dateadd(day, seq4(), '{{ start_date }}'::date) <= '{{ end_date }}'::date
    )
    select * from date_spine
{% endmacro %}
