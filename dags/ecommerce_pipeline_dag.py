from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'hamayun',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'olist_ecommerce_ingestion_dag',
    default_args=default_args,
    description='Pipeline to extract PostgreSQL and MongoDB data into raw Parquet files',
    schedule='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    run_extraction = BashOperator(
        task_id='extract_sources_to_raw',
        bash_command='cd /opt/airflow/project && python extract_to_raw.py',
    )

    run_extraction 