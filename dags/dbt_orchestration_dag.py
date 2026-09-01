from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'hamayun',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'olist_end_to_end_pipeline',
    default_args=default_args,
    description='End-to-end Olist data ingestion and dbt transformation pipeline',
    schedule='@daily',
    catchup=False,
) as dag:

    extract_sources = BashOperator(
        task_id='extract_sources_to_raw',
        bash_command='cd /opt/airflow/project && python extract_to_raw.py',
    )

    # Task 3: Run dbt models
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/project/dbt_ecommerce && dbt run --profiles-dir /opt/airflow/project',
    )

    # Task 4: Test dbt models
    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/project/dbt_ecommerce && dbt test --profiles-dir /opt/airflow/project',
    )

    extract_sources >> dbt_run >> dbt_test