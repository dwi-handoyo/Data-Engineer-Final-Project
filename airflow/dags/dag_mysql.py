#!python airflow

from datetime import datetime
from datetime import timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from airflow.utils.dates import days_ago

default_args = {
    'owner': 'handoyo'}

dag = DAG(
    dag_id='home_credit_application_mysql',
    start_date=days_ago(1),
    schedule_interval= None, #unscheduled, triggered manually
    default_args=default_args)

t1 = DummyOperator(
    task_id='Start')

t2 = BashOperator(
    task_id='Import_CSV_To_MySQL',
    bash_command='python /usr/local/spark/app/import_csv_to_mysql.py',
    dag=dag)

t3 = BashOperator(
    task_id='Export_MySQL_To_PostgreSQL',
    bash_command='python /usr/local/spark/app/export_mysql_to_postgresql.py',
    dag=dag)

t4 = BashOperator(
    task_id='Preprocessing_Logistic_Regression',
    bash_command='python /opt/airflow/scripts/ML/preprocessing_and_lr.py',
    dag=dag)

t5 = DummyOperator(
    task_id='Stop')

t1 >> t2 >> t3 >> t4 >> t5