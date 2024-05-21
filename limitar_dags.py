from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from datetime import datetime, timedelta
import time

default_args = {
    'owner': 'Felipe Test',
    'depends_on_past': False,
    'start_date': days_ago(0), 
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
}

resource_config = {"KubernetesExecutor": {"request_memory": "200Mi", # 200Mebibytes
                                          "limit_memory": "200Mi", 
                                          "request_cpu": "200m",  #200 milicores o 0.2CPU
                                          "limit_cpu": "200m"}}

def print_numbers():
    for i in range(1, 11):
        time.sleep(3)
        print(i)




with DAG(dag_id='Delimiar_recursos', schedule_interval=None, 
         tags=['analytics'], default_args=default_args) as dag:
    
    task = PythonOperator(
        task_id='ejemplo_task_delimitado',
        python_callable=print_numbers,
        #op_args=[20,timetask],
        start_date=days_ago(0),
        owner='airflow',
        executor_config = resource_config
    )

    task






# https://towardsdatascience.com/why-we-must-choose-kubernetes-executor-for-airflow-28176062a91b    