from airflow import DAG
from airflow.operators.bash import BashOperator  # type: ignore[import-not-found]
from airflow.operators.python import PythonOperator  # type: ignore[import-not-found]
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from load_to_duckdb import load_data

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'crm_sales_etl_pipeline_',
    default_args=default_args,
    description='ETL pipeline for CRM Sales data using DuckDB and dbt inside Docker',
    schedule=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    load_csv = PythonOperator(
        task_id='load_csv_to_duckdb',
        python_callable=load_data,
    )

    # مسار dbt الصحيح داخل حاوية Astro
    dbt_dir = '/usr/local/airflow/dbt_project'
    
    run_dbt = BashOperator(
        task_id='run_dbt_models',
        bash_command=f'cd {dbt_dir} && dbt run --profiles-dir /usr/local/airflow/include',
    )

    test_dbt = BashOperator(
        task_id='test_dbt_models',
        bash_command=f'cd {dbt_dir} && dbt test --profiles-dir /usr/local/airflow/include',
    )

    load_csv >> run_dbt >> test_dbt