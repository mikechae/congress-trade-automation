from sqlalchemy import MetaData, Table, Column, String, create_engine
from secrets_1 import *

def make_table():
    conn_str = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'
    db = create_engine(conn_str) 
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

