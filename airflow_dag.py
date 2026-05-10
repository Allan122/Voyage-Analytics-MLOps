from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'voyage_admin',
    'depends_on_past': False,
    'start_date': datetime(2026, 5, 9),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'voyage_mlops_pipeline',
    default_args=default_args,
    description='Automated MLOps pipeline for Travel Analytics',
    schedule_interval=timedelta(days=1),
)

def extract_and_clean_data():
    print("Extracting and cleaning daily travel data...")

def train_regression_model():
    print("Training Flight Price Regression Model...")

def deploy_model():
    print("Deploying updated model to production...")

task_extract = PythonOperator(task_id='extract_data', python_callable=extract_and_clean_data, dag=dag)
task_train = PythonOperator(task_id='train_model', python_callable=train_regression_model, dag=dag)
task_deploy = PythonOperator(task_id='deploy_model', python_callable=deploy_model, dag=dag)

# Define the workflow order
task_extract >> task_train >> task_deploy