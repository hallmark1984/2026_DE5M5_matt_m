import pandas as pd
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine

env = {
    'paths': ['raw/03_Library Systembook.csv','raw/03_Library SystemCustomers.csv','logs'],
    'element': ['library_stuff', 'library_users','library_logs'],
    'rows_dropped' : [None,None,None],
    'rows_input' : [None,None,None],
    'rows_output' : [None,None,None],
    'start_time': [None,None,None],
    'end_time': [None,None,None],
}

ingest_loans_dtypes = {
    'Id':"Int64",
    'Books': str,
    'Days allowed to borrow':str,
    'Customer ID':"Int64"
}

def storage(frame, location):
    frame.to_csv(location,index=False)

def drop_null_records(df):
    return df.dropna()

def rename_cols(frame):
    old_cols = frame.columns
    for c in frame.columns:
        frame[c.replace(' ','').lower()] = frame[c]

    frame = frame.drop(old_cols, axis=1)
    return frame

def clean_dates(frame, date_cols=None):
    if date_cols == None:
        return frame
    df = frame.map(lambda x: x.replace('"', '') if isinstance(x, str) else x)
    df = df.map(lambda x: x.replace('"', '') if isinstance(x, str) else x)
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df 

def store_in_db(df, tablename):
    server = "localhost"
    database = "library_stuff"

    connection_string = (
            f"mssql+pyodbc://@{server}/{database}"
                "?driver=ODBC+Driver+17+for+SQL+Server"
                    "&trusted_connection=yes"
                    )

    engine = create_engine(connection_string)
    df.to_sql(tablename, engine, if_exists="append",   index=False)


def overlord(env_var=env, element_index=0):
    env_var['start_time'][element_index] = datetime.now()
    if element_index == 2:
        print(element_index)
        env_var['rows_input'][element_index] = 1
        env_var['rows_output'][element_index] = 1
        
        env_var['rows_dropped'][element_index] = 0
        env_var['end_time'][element_index] = datetime.now()
        logs = pd.DataFrame(env_var)
        logs = logs[logs['paths']!='logs']
        logs['rundate'] = datetime.now().strftime('%Y%m%d')
        store_in_db(logs, env_var['element'][element_index])
        return
    
    if element_index == 0:
        date_cols = ['Book checkout','Book Returned']
    else:
        date_cols = None

    df = pd.read_csv(env_var['paths'][element_index])
    

    env_var['rows_input'][element_index] = len(df)
    df = clean_dates(df,date_cols)
    df = rename_cols(df)
    df = drop_null_records(df)

    df['rundate'] = datetime.now().strftime('%Y%m%d')
    env_var['rows_dropped'][element_index] = env_var['rows_input'][element_index]-len(df)
    env_var['end_time'][element_index] = datetime.now()
    env_var['rows_output'][element_index] = len(df)
    store_in_db(df, env_var['element'][element_index])
    return


if __name__ == 'main':
    for i in range(3):
        # 1and 2 run ingest and clean, 3 stores logs
        test_load = overlord(env, i)
