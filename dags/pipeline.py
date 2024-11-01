import os
from datetime import datetime, timedelta

from airflow.operators.python_operator import PythonOperator
from dotenv import load_dotenv

from airflow import DAG
from data_ingestion.scraper import scrape_data

# Load environment variables
load_dotenv()

# Snowflake connection parameters
SNOWFLAKE_CONN_ID = "snowflake_default"
WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
DATABASE = "DAMG_7245_A3"
SCHEMA = "PUBLIC"

# S3 details
BUCKET_NAME = "damg7245-a3-store"
IMAGE_S3_PREFIX = "cfa-publications/images"
PDF_S3_PREFIX = "cfa-publications/pdfs"

# Local directories
IMAGE_DIRECTORY = "/opt/dags/images"
PDF_DIRECTORY = "/opt/dags/pdfs"

SEED_URL = "https://rpc.cfainstitute.org/en/research-foundation/publications#sort=%40officialz32xdate%20descending&numberOfResults=50&f:SeriesContent=[Research%20Foundation]"


# default_args = {
#     'owner': 'airflow',
#     'depends_on_past': False,
#     'start_date': datetime.now(),
#     'email_on_failure': False,
#     'email_on_retry': False,
#     'retries': 1,
#     'retry_delay': timedelta(minutes=5),
# }
#
# dag = DAG(
#     'cfa_publications_pipeline',
#     default_args=default_args,
#     description='A pipeline to process CFA publications',
#     schedule_interval=None
# )
#
# def download_and_save_articles(**kwargs):
#     url = "https://rpc.cfainstitute.org/en/research-foundation/publications#sort=%40officialz32xdate%20descending&numberOfResults=50&f:SeriesContent=[Research%20Foundation]"
#     articles = extract_article_details_and_files(url)
#
#     # Save the articles data to a JSON file
#     output_file = '/opt/dags/articles_data.json'
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(articles, f, ensure_ascii=False, indent=4)
#
#     print(f"Articles data saved to {output_file}")
#
# def upload_to_s3_and_update_links(**kwargs):
#     # Load the articles data
#     input_file = '/opt/dags/articles_data.json'
#     with open(input_file, 'r', encoding='utf-8') as f:
#         articles = json.load(f)
#
#     # Update article links and upload to S3
#     updated_articles = update_article_links(articles, IMAGE_DIRECTORY, PDF_DIRECTORY, BUCKET_NAME, IMAGE_S3_PREFIX, PDF_S3_PREFIX)
#
#     # Save the updated articles data
#     output_file = '/opt/dags/updated_articles_data.json'
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(updated_articles, f, ensure_ascii=False, indent=4)
#
#     print(f"Updated articles data saved to {output_file}")
#
# def insert_to_snowflake(**kwargs):
#     json_file_path = '/opt/dags/updated_articles_data.json'
#     insert_articles_from_json(json_file_path)
#
# # Define tasks
# download_task = PythonOperator(
#     task_id='download_articles',
#     python_callable=download_and_save_articles,
#     provide_context=True,
#     dag=dag,
# )
#
# upload_task = PythonOperator(
#     task_id='upload_to_s3',
#     python_callable=upload_to_s3_and_update_links,
#     provide_context=True,
#     dag=dag,
# )
#
# snowflake_task = PythonOperator(
#     task_id='insert_to_snowflake',
#     python_callable=insert_to_snowflake,
#     provide_context=True,
#     dag=dag,
# )
#
# # Set task dependencies
# download_task >> upload_task >> snowflake_task


with DAG(
    "data_scraper_dag",
    start_date=datetime.now(),
    max_active_runs=1,
    schedule_interval=None,
    default_args={"retries": 1, "retry_delay": timedelta(minutes=5), "owner": "me"},
    catchup=False,
) as dag:
    scraper_task = PythonOperator(
        task_id="scraper", python_callable=scrape_data, params={"seed_url": SEED_URL}
    )


with DAG():
    ...
