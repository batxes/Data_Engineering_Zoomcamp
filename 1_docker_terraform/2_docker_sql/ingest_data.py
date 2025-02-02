#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
import pyarrow.parquet as pq
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'output.parquet' # yellow taxi data is in parquet format

    # Download the parquet file
    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    parquet_file = pq.ParquetFile(csv_name)

    # Iterate through the parquet file in chunks
    for i, batch in enumerate(parquet_file.iter_batches(batch_size=100000)):
        print (f"Processing batch {i}")
        chunk = pd.DataFrame(batch.to_pandas())
        # Process your chunk here
        chunk.tpep_pickup_datetime = pd.to_datetime(chunk.tpep_pickup_datetime)
        chunk.tpep_dropoff_datetime = pd.to_datetime(chunk.tpep_dropoff_datetime)
        chunk.to_sql(name=table_name, con=engine, if_exists='append')

    print("Data ingestion completed")

    # code for zones ingestion
    #zones_url = 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv'
    #zones_csv_name = 'zones.csv'
    #os.system(f"wget {zones_url} -O {zones_csv_name}")
    #zones_df = pd.read_csv(zones_csv_name)
    #zones_df.to_sql(name='zones', con=engine, if_exists='replace')
    #print("Zones ingestion completed")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest parquet file into Postgres')

    parser.add_argument('--user', help='user name for postgres')           
    parser.add_argument('--password', help='password for postgres')     
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the parquet file')

    args = parser.parse_args()

    main(args)



