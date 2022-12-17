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
    dag_id='zips_companies_mongodb',
    start_date=days_ago(1),
    schedule_interval= None, #unscheduled, triggered manually
    default_args=default_args)

t1 = DummyOperator(
    task_id='Start')

t2 = BashOperator(
    task_id='Zips_Data_Transform',
    bash_command='python /opt/airflow/scripts/transform_zips.py',
    dag=dag)

t3 = BashOperator(
    task_id='Companies_Data_Transform',
    bash_command='python /opt/airflow/scripts/transform_companies.py',
    dag=dag)

t4 = BashOperator(
    task_id='Update_Dim_Country',
    bash_command='python /opt/airflow/scripts/dim_country.py',
    dag=dag)

t5 = BashOperator(
    task_id='Update_Dim_State',
    bash_command='python /opt/airflow/scripts/dim_state.py',
    dag=dag)

t6 = BashOperator(
    task_id='Update_Dim_City',
    bash_command='python /opt/airflow/scripts/dim_city.py',
    dag=dag)

t7 = BashOperator(
    task_id='Update_City_Office_Per_State',
    bash_command='python /opt/airflow/scripts/fact_city_office_per_state.py',
    dag=dag)

t8 = DummyOperator(
    task_id='Stop')

t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7 >> t8