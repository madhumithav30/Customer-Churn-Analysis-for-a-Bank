from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'Senior_Data_Engineer',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'canadian_bank_retention_pipeline',
    default_args=default_args,
    description='Medallion Pipeline for Churn Risk Scoring',
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task 1: Silver Layer Transformation
    t1 = BashOperator(
        task_id='spark_bronze_to_silver',
        bash_command='spark-submit /opt/airflow/jobs/silver_layer.py'
    )

    # Task 2: Gold Layer Transformation
    t2 = BashOperator(
        task_id='spark_silver_to_gold',
        bash_command='spark-submit /opt/airflow/jobs/gold_layer.py'
    )

    t1 >> t2