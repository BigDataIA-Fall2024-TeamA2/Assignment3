import os
import json
from dotenv import load_dotenv
import snowflake.connector
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get Snowflake connection parameters from environment variables
account = os.getenv('SNOWFLAKE_DB_ACCOUNT')
user = os.getenv('SNOWFLAKE_DB_USER')
password = os.getenv('SNOWFLAKE_DB_PASSWORD')
database = "DAMG_7245_A3"
warehouse = "MY_WAREHOUSE"  # Make sure this is set in your .env file

# Function to convert date string to Snowflake-compatible format
def convert_date(date_string):
    try:
        date_object = datetime.strptime(date_string, '%d %b %Y')
        return date_object.strftime('%Y-%m-%d')
    except ValueError:
        return None

# Function to insert an article
def insert_article(cursor, article):
    insert_query = """
    INSERT INTO ARTICLES (TITLE, DESCRIPTION, PUBLICATION_DATE, AUTHORS, PDF_URL, IMAGE_URL)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    converted_date = convert_date(article['date'])
    cursor.execute(insert_query, (
        article['title'],
        article['description'],
        converted_date,
        article['authors'],
        article['pdf_url'],
        article['image_url']
    ))

def insert_articles_from_json(json_file_path):
    # Establish connection to Snowflake
    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
        database=database,
        warehouse=warehouse
    )

    cursor = conn.cursor()

    try:
        # Explicitly set the warehouse and schema
        cursor.execute(f"USE WAREHOUSE {warehouse}")
        cursor.execute(f"USE SCHEMA {database}.PUBLIC")  # Assuming PUBLIC schema, adjust if different

        # Check if the table exists and has content
        cursor.execute("SHOW TABLES LIKE 'ARTICLES'")
        table_exists = cursor.fetchone() is not None

        if table_exists:
            cursor.execute("SELECT COUNT(*) FROM ARTICLES")
            row_count = cursor.fetchone()[0]
            if row_count > 0:
                # Truncate the table if it has content
                cursor.execute("TRUNCATE TABLE ARTICLES")
                print("Existing data in ARTICLES table has been truncated.")
        else:
            # Create the table if it doesn't exist
            create_table_query = """
            CREATE TABLE IF NOT EXISTS ARTICLES (
                TITLE STRING,
                DESCRIPTION STRING,
                PUBLICATION_DATE DATE,
                AUTHORS STRING,
                PDF_URL STRING,
                IMAGE_URL STRING
            )
            """
            cursor.execute(create_table_query)
            print("ARTICLES table created.")

        # Load articles from JSON file
        with open(json_file_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)

        # Insert all articles
        for article in articles:
            insert_article(cursor, article)

        # Commit the changes
        conn.commit()
        print("Data inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        # Close cursor and connection
        cursor.close()
        conn.close()


def get_all_articles():
    # Establish connection to Snowflake
    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
        database=database,
        warehouse=warehouse
    )

    cursor = conn.cursor()
    # Explicitly set the warehouse and schema
    cursor.execute(f"USE WAREHOUSE {warehouse}")
    cursor.execute(f"USE SCHEMA {database}.PUBLIC")  # Assuming PUBLIC schema, adjust if different
    get_query = "SELECT A_ID, PDF_URL, IMAGE_URL FROM ARTICLES"

    result = cursor.execute(get_query)
    return result.fetchall()



if __name__ == "__main__":
    # Specify the path to your JSON file
    json_file_path = r"D:\Projects\Assignment3\dags\updated_articles_data.json"
    insert_articles_from_json(json_file_path)
