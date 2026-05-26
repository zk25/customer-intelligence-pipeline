from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'data_team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def run_pyspark():
    result = subprocess.run(
        ["python", "spark/eda.py"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(result.stderr)

def run_mlflow():
    result = subprocess.run(
        ["python", "mlflow/train.py"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(result.stderr)

def validate_output():
    import pandas as pd
    import os
    assert os.path.exists("data/processed/rfm_features"), "RFM output missing!"
    df = pd.read_parquet("data/processed/rfm_features")
    assert len(df) > 0, "RFM output is empty!"
    print(f"Validation passed: {len(df)} rows found")

with DAG(
    dag_id='weekly_pipeline',
    default_args=default_args,
    schedule_interval='@weekly',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['production']
) as dag:

    t1 = PythonOperator(
        task_id='run_pyspark_eda',
        python_callable=run_pyspark
    )
    t2 = PythonOperator(
        task_id='validate_output',
        python_callable=validate_output
    )
    t3 = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/airflow/dags && dbt run --project-dir /dbt/olist_pipeline'
    )
    t4 = BashOperator(
        task_id='dbt_test',
        bash_command='cd /opt/airflow/dags && dbt test --project-dir /dbt/olist_pipeline'
    )
    t5 = PythonOperator(
        task_id='retrain_model',
        python_callable=run_mlflow
    )

    t1 >> t2 >> t3 >> t4 >> t5