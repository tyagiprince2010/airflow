import airflow
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.contrib.kubernetes.secret import Secret
from datetime import timedelta


default_args = {
    'start_date': airflow.utils.dates.days_ago(0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'test_kube',
    default_args=default_args,
    description='Kubernetes Operator desc dag',
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=60))

secret_env = Secret(
    deploy_type = 'env',
    deploy_target = 'GOOGLE_APPLICATION_CREDENTIALS',
    secret = 'airflow-testing-secret',
    key = 'key.json'
)



py_test_k8_task1 = KubernetesPodOperator(namespace='airflow-test',
                          image="gcr.io/propertyguru-datalake-v0/dsa/airflow:python37", #Image path was incorrect
                          cmd=["/bin/bash", "-c"],
                          arguments=["python", "./prog/py_test.py"],
                          name="test-kube",
                          secrets=[secret_env],
                          in_cluster=True, #To trigger cluster kubeconfig.
                          image_pull_policy="Always",  #In my case, I need the image update to occur whenever there is an update
                          task_id="py_test_k8_task1",
                          is_delete_operator_pod=True,
                          hostnetwork=False,
                          dag=dag
                          )


py_test_k8_task2 = KubernetesPodOperator(namespace='airflow-test',
                          image="gcr.io/propertyguru-datalake-v0/dsa/airflow:python37", #Image path was incorrect
                          cmd=["/bin/bash", "-c"],
                          arguments=["python", "./prog/py_test.py"],
                          name="test-kube",
                          secrets=[secret_env],
                          in_cluster=True, #To trigger cluster kubeconfig.
                          image_pull_policy="Always",  #In my case, I need the image update to occur whenever there is an update
                          task_id="py_test_k8_task2",
                          is_delete_operator_pod=True,
                          hostnetwork=False,
                          dag=dag
                          )

py_test_k8_task1 >> py_test_k8_task2
