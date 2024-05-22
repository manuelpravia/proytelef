import time
from datetime import datetime, timedelta

from airflow import DAG
from airflow.exceptions import AirflowFailException
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.contrib.operators.ssh_operator import SSHOperator


dag_args = {
    "depends_on_past": False,
    "email": ["test@test.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function, # or list of functions
    # 'on_success_callback': some_other_function, # or list of functions
    # 'on_retry_callback': another_function, # or list of functions
    # 'sla_miss_callback': yet_another_function, # or list of functions
    # 'trigger_rule': 'all_success'
}

dag = DAG(
    "Ejecutar_script_en_multiples_servidores",
    description="Mi primer DAG",
    default_args=dag_args,
    schedule_interval=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["load-data"],
    params={"commit": "000000","branch":"feacture1"}
)

def tarea0_func(**kwargs):
    conf = kwargs['dag_run'].conf
    print("ejecutando tarae0: inicio de ejecucion")
    time.sleep(5)
    if "commit" in conf and conf["commit"]=="1":
       raise AirflowFailException("Permisos insuficientes para ejecutar el commit 1")

    print("ejecucion de tarea0: fin de la ejecucion")
    return { "ok": 1 }

def tarea2_func(**kwargs):
    xcom_value = kwargs['ti'].xcom_pull(task_ids='tarea0')
    print("ejecutando tarae2: inicio de ejecucion")
    time.sleep(10)
    print( "Hola" )
    print( xcom_value )
    time.sleep(5)
    print("ejecucion de tarea2: fin de la ejecucion")
    return { "ok": 2 }

def tarea3_func(**kwargs):
    xcom_value = kwargs['ti'].xcom_pull(task_ids='tarea2')
    print("ejecutando tarae3: inicio de ejecucion")
    time.sleep(5)
    print( "Hola" )
    print( xcom_value )
    time.sleep(10)
    print("ejecucion de tarea3: fin de la ejecucion")
    return { "ok": 3 }


tarea2 = PythonOperator(
    task_id='tarea2',
    python_callable=tarea2_func,
    dag=dag
)

tarea3 = PythonOperator(
    task_id='tarea3',
    python_callable=tarea3_func,
    dag=dag
)


tarea1 = SSHOperator(
    task_id='ejecutando_script_de_serv1_a_serv2',
    ssh_conn_id='my_ssh_conn',  # Nombre de tu conexión SSH configurada en Airflow
    command='python3 /root/ejecutar_servido2.py',  # Ruta al script de Python en el servidor remoto
    #params={'origen': 'Airflow container', 'destino': 'servidor remoto 1'},  # Parámetros que deseas enviar al script
    cmd_timeout=120,
    do_xcom_push=True,  # Permite que la salida de la tarea se almacene en XCom para verla en la interfaz de Airflow
    dag=dag,
)

tarea2 >>  tarea1 >> tarea3 

