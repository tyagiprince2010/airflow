import datetime
from airflow import models
from airflow.contrib.kubernetes import pod
from airflow.contrib.kubernetes import secret
from airflow.contrib.operators import kubernetes_pod_operator



with DAG('test_kube', default_args=default_args, description='Kubernetes Operator',
         schedule_interval='00 12 01 * *') as dag:
    k = KubernetesPodOperator(namespace='default',
                              image="gcr.io/propertyguru-datalake-v0/dsa/airflow:python37", #Image path was incorrect
                              name="test",
                              in_cluster=True, #To trigger cluster kubeconfig.
                              image_pull_policy="Always",  #In my case, I need the image update to occur whenever there is an update
                              task_id="test",
                              is_delete_operator_pod=False,
                              hostnetwork=False,
                              dag=dag
                              )
