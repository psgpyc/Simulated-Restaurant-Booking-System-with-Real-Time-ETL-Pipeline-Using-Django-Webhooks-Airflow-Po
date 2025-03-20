import os
from datetime import timedelta
from pendulum import datetime
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook


from helpers.checkers import validate_json_orders

os.environ['NO_PROXY'] = '*'


default_args = {
    'owner': 'psgpyc',
    'retries': 3, 
    'retry_delay': timedelta(minutes=3)

}


dag_defination = """ 
    This DAG extracts order data when the orders have been placed
"""


@dag(
    dag_id="order_pipeline_dag",
    default_args=default_args,
    start_date=datetime(2025, 3, 16),
    schedule=None,
    tags= ['etl', 'orders'],
    catchup=False)
def etl_process_order_data():
    @task()
    def extract(**kwargs):
        print('From the pipeline')
        dag_run_conf = kwargs["dag_run"].conf
        return dag_run_conf
    
    @task()
    def transform(payload):
        validated_data = validate_json_orders(payload)
        print('from transform ..................')
        order_items = validated_data.pop('order_items')

        for each in order_items:
            each['order_id'] = validated_data['order_id']
            each['customer_id'] = validated_data['customer_id']

        return {'order': validated_data, 'orderitems': order_items}
    

    @task()
    def load_order(payload):
        order_data = payload.pop('order')
        pg_hook = PostgresHook(postgres_conn_id='order_management_conn')

        sql = """
        INSERT INTO orders (order_id, customer_id, created_on, updated_on, total_price, is_completed) 
        VALUES (
            %(order_id)s,
            %(customer_id)s,
            %(ordered_on)s,
            %(updated_on)s,
            %(total_price)s,
            %(order_status)s
        )
        ON CONFLICT 
            (order_id) 
        DO UPDATE
        SET
            updated_on=EXCLUDED.updated_on,
            total_price=EXCLUDED.total_price,
            is_completed=EXCLUDED.is_completed

        """

        pg_hook.run(sql, parameters=order_data)

    @task()
    def load_order_items(payload):
        order_items = payload.pop('orderitems')
        pg_hook = PostgresHook(postgres_conn_id='order_management_conn')
        for each_item in order_items:
            sql = """
            INSERT INTO orderitems (order_id, customer_id, menu_item, quantity)
            VALUES (
                %(order_id)s,
                %(customer_id)s,
                %(menu_item)s,
                %(quantity)s
            )
            ON CONFLICT 
                (order_id, customer_id, menu_item)
            DO UPDATE
            SET
                quantity=orderitems.quantity + EXCLUDED.quantity
            """
            pg_hook.run(sql, parameters=each_item)

    extracted_data  = extract()
    transformed_data = transform(extracted_data)
    load_order(transformed_data)
    load_order_items(transformed_data)


etl_process_order_data()