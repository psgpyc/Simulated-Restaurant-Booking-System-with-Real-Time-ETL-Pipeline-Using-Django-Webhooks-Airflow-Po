import os
import pendulum
from helpers.checkers import validate_json
from datetime import timedelta
from airflow.providers.postgres.hooks.postgres import PostgresHook
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
def etl_process_reservation_data():
    @task()
    def extract(**kwargs):
        """Extract data from the webhook payload"""
        dag_run_conf = kwargs["dag_run"].conf
        return dag_run_conf
    
    @task()
    def transform(payload):
        validated_data = validate_json(payload)
        if validated_data:
            customers = validated_data.pop('guest')
            validated_data['customer_id'] = customers['customer_id']
            reservation = validated_data

            return {'customers_data': customers, 'reservation_data': reservation}
        

        
    @task()
    def load_customers(transformed_payload):
        customer = transformed_payload.get('customers_data', {})

        pg_hook = PostgresHook(postgres_conn_id='order_management_conn')
        sql = """
            INSERT INTO customers (customer_id, customer_name, customer_email, customer_phone, joined_date)
            VALUES (%(customer_id)s, %(customer_name)s, %(customer_email)s, %(customer_phone)s, %(joined_date)s)
            ON CONFLICT (customer_id) DO UPDATE SET 
                customer_name = EXCLUDED.customer_name,
                customer_email = EXCLUDED.customer_email,
                customer_phone = EXCLUDED.customer_phone,
                joined_date = EXCLUDED.joined_date;

            """
        pg_hook.run(sql, parameters=customer)
        return 'Success'
    
    @task


    def load_reservations(transformed_payload):
        reservation = transformed_payload.get('reservation_data', {}) 

        pg_hook = PostgresHook(postgres_conn_id='order_management_conn')
        sql = """
            INSERT INTO reservations (
                reservation_id, customer_id, reservation_time, experience, size, status, payment_mode, visit_notes, created_at, source
            )
            VALUES (
                %(reservation_id)s,
                %(customer_id)s,
                %(reservation_time)s,
                %(experience)s,
                %(size)s,
                %(status)s,
                %(payment_mode)s,
                %(visit_notes)s,
                %(created_at)s,
                %(source)s
            )
            ON CONFLICT (reservation_id) DO UPDATE SET 
                reservation_time = EXCLUDED.reservation_time,
                experience = EXCLUDED.experience,
                size = EXCLUDED.size,
                status = EXCLUDED.status,
                payment_mode = EXCLUDED.payment_mode,
                visit_notes = EXCLUDED.visit_notes,
                created_at = EXCLUDED.created_at,
                source = EXCLUDED.source;
             """

        pg_hook.run(sql, parameters=reservation)
        


    received_data = extract()
    transformed_data = transform(payload = received_data)
    load_customers(transformed_payload=transformed_data)
    load_reservations(transformed_payload=transformed_data)


etl_process_reservation_data()






    



