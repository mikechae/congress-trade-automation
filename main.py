import requests, psycopg2, uuid
import pandas as pd
from secrets_1 import DB_USERNAME, DB_HOSTNAME, DB_NAME, DB_PASSWORD, DB_PORT
from sqlalchemy import create_engine, MetaData, Table, Column, String

link = 'https://senate-stock-watcher-data.s3-us-west-2.amazonaws.com/aggregate/all_transactions.json'

def get_data():
    try:
        response = requests.get(link).json()
        print('Stock Watcher API Status: '+ str(requests.get(link).status_code))
    except (requests.Timeout, requests.ConnectionError, requests.HTTPError, requests.RequestException) as error:
        print(error.strerror)
    finally:
        df = pd.json_normalize(response)
        Filepath = '/Users/mikechae/Projects/Senator automation/output.csv'
        df.to_csv(Filepath,index=False)

def db_connect():
    
    df = pd.read_csv('/Users/mikechae/Projects/Senator automation/output.csv')
    
    try:  
        #connecting to DB
        conn_str = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'
        db = create_engine(conn_str) 
        connection = db.connect()
        if connection:
            print("SQLAlchemy DB Connection Successful")
        else: raise Exception
    except: raise Exception

    #create target table
    meta = MetaData()
    senators_socks = Table(
        'senators_socks', meta, 
        #Column('uuid', String, primary_key = True), 
        Column('transaction_date', String),
        Column('owner', String),
        Column('ticker', String),
        Column('asset_description', String),
        Column('asset_type', String),
        Column('type', String),
        Column('amount', String),
        Column('comment', String),
        Column('party', String),
        Column('state', String),
        Column('industry', String),
        Column('sector', String),
        Column('senator', String),
        Column('ptr_link', String),
        Column('disclosure_date', String)
        )
    meta.create_all(db)
    connection.close

    #connect via psyocopg to insert new data
    with psycopg2.connect(conn_str) as conn:
        print("Psycopg DB Connection Successful")
    cursor = conn.cursor()

    #insert new data (append on conflict)
    df.to_sql('senators_socks',con=connection, if_exists='append', index=False)
    conn.autocommit = True

    #fetch data from DB to confirm write
    sql1 = '''SELECT * FROM senators_socks LIMIT 10;'''
    cursor.execute(sql1) 
    if cursor.fetchall():
        print('Success!')

    #close connection
    conn.close()


if __name__ == "__main__":
    get_data()
    db_connect()