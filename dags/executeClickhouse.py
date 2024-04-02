from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False, # if True, the task instance will run only if the previous task instance has succeeded
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5), # retry tasks after 5 seconds 
}

# Define the DAG 
dag = DAG(
    'deploy_project_kafkaClickhouse',
    default_args=default_args,
    description='Deploy Airflow',
    schedule_interval='30 9 * * *',  # Set schedule interval to run every 10 minutes
    start_date=datetime(2024, 3, 26),  # Set the start date
    catchup=False
)

# Define a function to print a message
def print_message(message):
    print(message)

# Task to print "Task 1 Executed" when executed
task1 = BashOperator(
    task_id='task_Clickhouse_Consumer',
    bash_command='python /opt/airflow/dags/clickhouse/consumer.py',
    dag=dag
)