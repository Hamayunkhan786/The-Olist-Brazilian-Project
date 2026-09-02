from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'hamayun',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email': ['hamayun@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'olist_end_to_end_pipeline',
    default_args=default_args,
    description='End-to-end Olist data ingestion, warehouse load, and dbt transformation pipeline',
    schedule='@daily',
    catchup=False,
    tags=['olist', 'data-warehouse', 'etl'],
) as dag:

    extract_sources = BashOperator(
        task_id='extract_sources_to_raw',
        bash_command='cd /opt/airflow/project && python extract_to_raw.py',
        pool='postgres_pool',
        pool_slots=1,
    )

    load_orders_to_snowflake = BashOperator(
        task_id='load_orders_to_snowflake',
        bash_command='cd /opt/airflow/project && python load_orders_to_snowflake.py',
        pool='snowflake_pool',
        pool_slots=1,
    )

    load_postgre_to_snowflake = BashOperator(
        task_id='load_postgre_to_snowflake',
        bash_command='cd /opt/airflow/project && python load_postgre_to_snowflake.py',
        pool='snowflake_pool',
        pool_slots=1,
    )

    load_mongo_to_snowflake = BashOperator(
        task_id='load_mongo_to_snowflake',
        bash_command='cd /opt/airflow/project && python load_mongo_to_snowflake.py',
        pool='snowflake_pool',
        pool_slots=1,
    )

    dbt_staging = BashOperator(
        task_id='dbt_staging',
        bash_command='cd /opt/airflow/project/dbt_ecommerce && dbt run --select staging --profiles-dir /opt/airflow/project',
        pool='dbt_pool',
        pool_slots=1,
    )

    dbt_marts = BashOperator(
        task_id='dbt_marts',
        bash_command='cd /opt/airflow/project/dbt_ecommerce && dbt run --select marts --profiles-dir /opt/airflow/project',
        pool='dbt_pool',
        pool_slots=1,
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/project/dbt_ecommerce && dbt test --profiles-dir /opt/airflow/project',
        pool='dbt_pool',
        pool_slots=1,
        retries=1,
    )

    dbt_docs = BashOperator(
        task_id='dbt_docs',
        bash_command='cd /opt/airflow/project/dbt_ecommerce && dbt docs generate --profiles-dir /opt/airflow/project',
        pool='dbt_pool',
        pool_slots=1,
        trigger_rule='all_done',
    )

    extract_sources >> [load_orders_to_snowflake, load_postgre_to_snowflake, load_mongo_to_snowflake]
    [load_orders_to_snowflake, load_postgre_to_snowflake, load_mongo_to_snowflake] >> dbt_staging
    dbt_staging >> dbt_marts
    dbt_marts >> dbt_test
    dbt_test >> dbt_docs