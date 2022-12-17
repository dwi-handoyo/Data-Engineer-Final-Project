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
    dag_id='currency_monthly',
    start_date=days_ago(1),
    schedule_interval='* * 1 * *', #setiap bulan tanggal 1 saat tengah malam
    default_args=default_args)

t1 = DummyOperator(
    task_id='Start')

t2 = BashOperator(
    task_id='Update_Dim_Currency',
    bash_command='python /opt/airflow/scripts/dim_currency.py',
    dag=dag)

t3 = BashOperator(
    task_id='Monthly_Currency_Avg',
    bash_command='python /opt/airflow/scripts/fact_currency_daily_avg.py',
    dag=dag)

t4 = DummyOperator(
    task_id='Stop')

t1 >> t2 >> t3 >> t4