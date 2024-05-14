

from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'execute_script_on_external_server',
    default_args=default_args,
    description='Execute a Python script on an external server via SSH',
    schedule_interval=None,
)

task = SSHOperator(
    task_id='execute_script',
    ssh_conn_id='my_ssh_conn',
    command='python3 /root/generar_data.py',  # Ruta al script en el servidor externo
    dag=dag,
)

task
