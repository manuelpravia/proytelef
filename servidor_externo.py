

from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 15),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'execute_sev_ewaya',
    default_args=default_args,
    description='Execute a Python script on an external server via SSH',
    schedule_interval=None,
)

task = SSHOperator(
    task_id='ejecuta_EWAYA',
    ssh_conn_id='conn_telefonica',
    cmd_timeout=60,
    command='python3 /datos/FG_DATOS/Shells/mensajes.py',  # Ruta al script en el servidor externo
    dag=dag,
)

task
