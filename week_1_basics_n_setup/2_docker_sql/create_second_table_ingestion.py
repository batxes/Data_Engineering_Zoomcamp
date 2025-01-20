#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db

    # create SQLAlchemy engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    zones_url = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv'
    zones_csv_name = 'zones.csv'
    os.system(f"wget {zones_url} -O {zones_csv_name}")
    zones_df = pd.read_csv(zones_csv_name)
    print (zones_df.head())
    zones_df.to_sql(name='zones', con=engine, if_exists='replace')
    print("Zones ingestion completed")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', required=True, help='username for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')

    args = parser.parse_args()

    main(args) 