import os
import pendulum
from datetime import timedelta
from airflow.decorators import task, dag

os.environ['NO_PROXY'] = '*'

default_agrs = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

dag_defination = """ 
    This DAG extracts data from multiple ordering platforms, transforms it, and loads it to a centralised database. 
"""

@dag(
    dag_id='etl_pipeline_dag',  
    default_args=default_agrs,
    schedule=None, 
    start_date= pendulum.datetime(2025, 3, 13, tz="UTC"),
    tags= ['etl', 'cont'],
    doc_md=dag_defination,
    catchup=False
)
def etl_process_order_data():
    @task()
    def extract(**kwargs):
        """Extract data from the webhook payload"""
        dag_run_conf = kwargs["dag_run"].conf
        print(f"Received webhook data:{dag_run_conf}")
        return dag_run_conf
    

    received_data = extract()
    print(received_data)


etl_process_order_data()






    




