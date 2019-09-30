from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta, datetime


default_args = {
    'start_date': datetime.now() - timedelta(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'airflow_test2',
    default_args=default_args,
    description='testing 2 parallel Mixed tasks',
    schedule_interval='*/2 * * * *',
    dagrun_timeout=timedelta(minutes=60))

# priority_weight has type int in Airflow DB, uses the maximum.
t1 = BashOperator(
    task_id='echo',
    bash_command='echo test',
    dag=dag,
    depends_on_past=False)


def print_context(ds, **kwargs):
    print(kwargs)
    print(ds)
    print("test 2")
    return 'Whatever you return gets printed in the logs'


t2 = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag)

t1 >> t2
