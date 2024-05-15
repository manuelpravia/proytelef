from airflow import DAG
from airflow.contrib.operators.ssh_operator import SSHOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 15),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'my_ssh_python_dag',
    default_args=default_args,
    description='A simple DAG to execute a Python script remotely and monitor the log in real time',
    schedule_interval='@once',
)

def print_numbers():
    for i in range(1, 21):
        print(i)

t1 = SSHOperator(
    task_id='ssh_task',
    ssh_conn_id='my_ssh_conn',  # Nombre de tu conexión SSH configurada en Airflow
    command='python3 /root/generar_data.py',  # Ruta al script de Python en el servidor remoto
    timeout=20,
    poke_interval=4,
    do_xcom_push=True,  # Permite que la salida de la tarea se almacene en XCom para verla en la interfaz de Airflow
    dag=dag,
)

t2 = PythonOperator(
    task_id='print_numbers_task',
    python_callable=print_numbers,
    dag=dag,
)



t1 >> t2
