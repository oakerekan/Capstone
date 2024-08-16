from airflow import DAG
from airflow.providers.google.cloud.transfers.postgres_to_gcs import (
    PostgresToGCSOperator,
)
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import (
    GCSToBigQueryOperator,
)
from datetime import datetime, timedelta
import logging
# Bigquery config variables
BQ_CONN_ID = "gcpconn"
GCS_PROJECT = "postgres-gcs"
BQ_DATASET = "Etl_capstone"
BQ_TABLE = "Table_capstone"
GCS_BUCKET = "etl_bucket_capstone"
# Postgres config variables
PG_CONN_ID = "Capstoneconn"
PG_SCHEMA = "brazilian_ecommerce"
tables = [
    "customers",
    "geolocation",
    "order_items",
    "order_payments",
    "order_reviews",
    "orders",
    "products",
    "sellers",
    "product_category_name_translation",
]
# Define schemas for each table
table_schemas = {
    "customers": [
        {"name": "customer_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "customer_unique_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "customer_zip_code_prefix", "type": "STRING", "mode": "NULLABLE"},
        {"name": "customer_city", "type": "STRING", "mode": "NULLABLE"},
        {"name": "customer_state", "type": "STRING", "mode": "NULLABLE"},
    ],
    "geolocation": [
        {"name": "geolocation_zip_code_prefix", "type": "STRING", "mode": "NULLABLE"},
        {"name": "geolocation_lat", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "geolocation_lng", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "geolocation_city", "type": "STRING", "mode": "NULLABLE"},
        {"name": "geolocation_state", "type": "STRING", "mode": "NULLABLE"},
    ],
    "order_items": [
        {"name": "order_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "order_item_id", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "product_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "seller_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "shipping_limit_date", "type": "TIMESTAMP", "mode": "NULLABLE"},
        {"name": "price", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "freight_value", "type": "FLOAT", "mode": "NULLABLE"},
    ],
    "order_payments": [
        {"name": "order_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "payment_sequential", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "payment_type", "type": "STRING", "mode": "NULLABLE"},
        {"name": "payment_installments", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "payment_value", "type": "FLOAT", "mode": "NULLABLE"},
    ],
    "order_reviews": [
        {"name": "review_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "order_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "review_score", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "review_comment_title", "type": "STRING", "mode": "NULLABLE"},
        {"name": "review_comment_message", "type": "text", "mode": "NULLABLE"},
        {"name": "review_creation_date", "type": "TIMESTAMP", "mode": "NULLABLE"},
        {"name": "review_answer_timestamp", "type": "TIMESTAMP", "mode": "NULLABLE"},
    ],
    "orders": [
        {"name": "order_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "customer_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "order_status", "type": "STRING", "mode": "NULLABLE"},
        {"name": "order_purchase_timestamp", "type": "TIMESTAMP", "mode": "NULLABLE"},
        {"name": "order_approved_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
        {
            "name": "order_delivered_carrier_date",
            "type": "TIMESTAMP",
            "mode": "NULLABLE",
        },
        {
            "name": "order_delivered_customer_date",
            "type": "TIMESTAMP",
            "mode": "NULLABLE",
        },
        {
            "name": "order_estimated_delivery_date",
            "type": "TIMESTAMP",
            "mode": "NULLABLE",
        },
    ],
    "products": [
        {"name": "product_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "product_category_name", "type": "STRING", "mode": "NULLABLE"},
        {"name": "product_name_lenght", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "product_description_lenght", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "product_photos_qty", "type": "INTEGER", "mode": "NULLABLE"},
        {"name": "product_weight_g", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "product_length_cm", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "product_height_cm", "type": "FLOAT", "mode": "NULLABLE"},
        {"name": "product_width_cm", "type": "FLOAT", "mode": "NULLABLE"},
    ],
    "sellers": [
        {"name": "seller_id", "type": "STRING", "mode": "NULLABLE"},
        {"name": "seller_zip_code_prefix", "type": "STRING", "mode": "NULLABLE"},
        {"name": "seller_city", "type": "STRING", "mode": "NULLABLE"},
        {"name": "seller_state", "type": "STRING", "mode": "NULLABLE"},
    ],
    "product_category_name_translation": [
        {"name": "product_category_name", "type": "STRING", "mode": "NULLABLE"},
        {"name": "product_category_name_english", "type": "STRING", "mode": "NULLABLE"},
    ],
}
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 8, 8),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}
dag = DAG(
    "extract_load_olist_dataset",
    default_args=default_args,
    description="Extract Olist data from PostgreSQL, load to GCS, and then to BigQuery",
    schedule_interval=None,
    catchup=False,
)
for table in tables:
    schema = table_schemas.get(table)
    logging.info(f"Starting extraction for table: {table}")
    if schema is None:
        logging.error(f"Schema for table: {table} is missing")
        raise ValueError(f"Schema for table: {table} is missing")
    postgres_to_gcs_task = PostgresToGCSOperator(
        task_id=f"extract_load_{table}_to_gcs",
        postgres_conn_id=PG_CONN_ID,
        gcp_conn_id=BQ_CONN_ID,
        sql=f'SELECT * FROM "{PG_SCHEMA}"."{table}";',
        bucket=GCS_BUCKET,
        filename=f"raw/{table}/{{{{ ds }}}}/{table}.csv",
        export_format="CSV",
        use_server_side_cursor=True,
        retries=2,
        retry_delay=timedelta(minutes=5),
        dag=dag,
    )
    gcs_to_bigquery_task = GCSToBigQueryOperator(
        task_id=f"gcs_to_bigquery_{table}",
        bucket=GCS_BUCKET,
        source_objects=[f"raw/{table}/{{{{ ds }}}}/{table}.csv"],
        destination_project_dataset_table=f"{GCS_PROJECT}.{BQ_DATASET}.{table}",
        create_disposition="CREATE_IF_NEEDED",
        write_disposition="WRITE_TRUNCATE",
        source_format="CSV",
        schema_fields=schema,
        gcp_conn_id=BQ_CONN_ID,
        dag=dag,
    )
    postgres_to_gcs_task >> gcs_to_bigquery_task