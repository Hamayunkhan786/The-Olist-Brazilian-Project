{# Macro: Generate Surrogate Key #}
{# Purpose: Create consistent surrogate keys across models #}
{# Usage: {{ generate_surrogate_key(['column1', 'column2']) }} #}

{% macro generate_surrogate_key(column_names) %}
    {% if execute %}
        {% set col_str = ', '.join(column_names) %}
    {% else %}
        {% set col_str = '' %}
    {% endif %}
    md5(cast(concat({{ col_str }}) as string))
{% endmacro %}


{# Macro: Format Timestamp #}
{# Purpose: Standardize timestamp formatting across models #}
{# Usage: {{ format_timestamp(column_name) }} #}

{% macro format_timestamp(column) %}
    to_timestamp_ntz({{ column }})
{% endmacro %}


{# Macro: Generate Date Dimension #}
{# Purpose: Create date spine for date dimension #}
{# Usage: {% set date_spine = generate_date_spine('2020-01-01', '2026-12-31') %} #}

{% macro generate_date_spine(start_date, end_date) %}
    with date_spine as (
        select 
            dateadd(day, seq4(), '{{ start_date }}'::date) as date_day
        from table(generator(rowcount => (datediff(day, '{{ start_date }}'::date, '{{ end_date }}'::date) + 1)))
        where dateadd(day, seq4(), '{{ start_date }}'::date) <= '{{ end_date }}'::date
    )
    select * from date_spine
{% endmacro %}
