import os
import requests
import pandas as pd
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

RAW_PATH = "/opt/airflow/raw_data"
CLEAN_PATH = "/opt/airflow/clean_data"
LOG_PATH = "/opt/airflow/clean_data/logs"


files = [
    "books_clean.csv",
    "customers_clean.csv",
]

def get_book_data(title):
    url = "https://openlibrary.org/search.json"
    params = {"title": title}
    print(f"Running: {title}")
    response = requests.get(url, params=params)
    data = response.json()
    if not data["docs"]:
        return None
    
    book = data["docs"][0]  # top match
    return {
            "title": book.get("title"),
            "author": book.get("author_name", []),
            "first_publish_year": book.get("first_publish_year"),
            "edition_count": book.get("edition_count"),
            "ratings_count": book.get("ratings_count", 0),
            "open_library_key": book.get("key")
            }

def collect_books():
    #path = CLEAN_PATH+'//'+files[0]
    path = os.path.join(CLEAN_PATH, files[0])
    df = pd.read_csv(path)
    df.to_csv(os.path.join(RAW_PATH, "ratings_raw.csv"))
    return 

def collect_ratings():
    try:
        path = os.path.join(RAW_PATH, 'ratings_raw')
        df = pd.read_csv(path)
        data = [get_book_data(book) for book in df['books'].unique()]
        book_df = pd.DataFrame(data)
        book_df.to_csv(os.path.join(CLEAN_PATH, "ratings_clean.csv"))

    except:
        data = [get_book_data(book) for book in ['Little Women','East of Eden','Catcher in the Rye']]
        book_df = pd.DataFrame(data)
        book_df.to_csv( os.path.join(CLEAN_PATH, "ratings_clean.csv"))

    return  

with DAG(
    dag_id="popularity_etl",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["library", "etl"],
) as dag:
    prepare_book_list = PythonOperator(
        task_id="prepare_book_list",
        python_callable=collect_books,
    )

    download_popularity = PythonOperator(
        task_id="download_popularity",
        python_callable=collect_ratings,
    )

    prepare_book_list >> download_popularity