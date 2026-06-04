import pandas as pd
from datetime import datetime
import os

from airflow import DAG
from airflow.operators.python import PythonOperator


RAW_PATH = "/opt/airflow/raw_data"
CLEAN_PATH = "/opt/airflow/clean_data"
LOG_PATH = "/opt/airflow/clean_data/logs"


files = [
    "03_Library Systembook.csv",
    "03_Library SystemCustomers.csv",
]


def ensure_dirs():
    os.makedirs(CLEAN_PATH, exist_ok=True)
    os.makedirs(LOG_PATH, exist_ok=True)


def clean_dataframe(df, date_cols=None):
    # rename columns
    df.columns = [c.replace(" ", "").lower() for c in df.columns]

    # remove quotes everywhere
    df = df.apply(lambda col: col.map(lambda x: x.replace('"', '') if isinstance(x, str) else x))

    # drop nulls
    df = df.dropna()

    # convert dates if needed
    if date_cols:
        for col in date_cols:
            if col.lower() in df.columns:
                df[col.lower()] = pd.to_datetime(df[col.lower()], errors="coerce")

    return df


def process_books():
    path = os.path.join(RAW_PATH, files[0])
    df = pd.read_csv(path)

    start = datetime.now()

    date_cols = ["Book checkout", "Book Returned"]
    df_clean = clean_dataframe(df, date_cols=date_cols)

    output_path = os.path.join(CLEAN_PATH, "books_clean.csv")
    df_clean.to_csv(output_path, index=False)

    log = pd.DataFrame([{
        "table": "library_books",
        "rows_input": len(df),
        "rows_output": len(df_clean),
        "rows_dropped": len(df) - len(df_clean),
        "start_time": start,
        "end_time": datetime.now(),
    }])

    log.to_csv(os.path.join(LOG_PATH, "books_log.csv"), index=False)


def process_customers():
    path = os.path.join(RAW_PATH, files[1])
    df = pd.read_csv(path)

    start = datetime.now()

    df_clean = clean_dataframe(df)

    output_path = os.path.join(CLEAN_PATH, "customers_clean.csv")
    df_clean.to_csv(output_path, index=False)

    log = pd.DataFrame([{
        "table": "library_customers",
        "rows_input": len(df),
        "rows_output": len(df_clean),
        "rows_dropped": len(df) - len(df_clean),
        "start_time": start,
        "end_time": datetime.now(),
    }])

    log.to_csv(os.path.join(LOG_PATH, "customers_log.csv"), index=False)


def final_log():
    logs = []

    for f in os.listdir(LOG_PATH):
        if f.endswith(".csv"):
            logs.append(pd.read_csv(os.path.join(LOG_PATH, f)))

    if logs:
        full_log = pd.concat(logs)
        full_log.to_csv(os.path.join(LOG_PATH, "final_log.csv"), index=False)


with DAG(
    dag_id="library_etl",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["library", "etl"],
) as dag:

    setup = PythonOperator(
        task_id="setup",
        python_callable=ensure_dirs,
    )

    books = PythonOperator(
        task_id="process_books",
        python_callable=process_books,
    )

    customers = PythonOperator(
        task_id="process_customers",
        python_callable=process_customers,
    )

    log = PythonOperator(
        task_id="final_log",
        python_callable=final_log,
    )

    setup >> [books, customers] >> log