
# Analytics Engineering

Before we start, I uploaded the data to GCS with the script in 3_data_warehouse/web_to_gcs.py
then I created a new dataset in BigQuery and loaded the data from GCS to BigQuery runnning this:

CREATE OR REPLACE EXTERNAL TABLE `dezoomcamp-ibai.trips_data_all.green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp_bigquery_week3_2025/green/green_tripdata_*.parquet']
);

CREATE OR REPLACE EXTERNAL TABLE `dezoomcamp-ibai.trips_data_all.yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp_bigquery_week3_2025/yellow/yellow_tripdata_*.parquet']
);

CREATE OR REPLACE EXTERNAL TABLE `dezoomcamp-ibai.trips_data_all.fhv_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp_bigquery_week3_2025/fhv/fhv_tripdata_*.parquet']
);
```

## Analytics Engineering Basics

https://www.youtube.com/watch?v=uF76d5EmdtU&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=41&ab_channel=DataTalksClub%E2%AC%9B

Analytics Engineering is the process of building data pipelines and tools that enable data-driven decision-making.

It is a combination of data engineering, data analysis, and data science.  

TOOLING:

Data Loading -> Data Storing -> Data modelling -> Data presentation

Data Storing:
- Clouda data warehouse slike Snowflake, BigQuery, Databricks, Redshift

Data modelling:
- Tools like dbt or Dataform

Data Presentation:
- BI tools like google data studio, Looker, Model or Tableau


## Data modelling concepts

Differences between ETL and ELT:
- ETL: Extract, Transform, Load
- ELT: Extract, Load, Transform

Kimballs Dimensional modelling:
- Star schema
- Snowflake schema
- Fact tables
- Dimension tables
- Slowly changing dimension (SCD)

## What is dbt?

https://www.youtube.com/watch?v=gsKuETFJr54&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=34&ab_channel=Victoria

dbt is a tool that allows you to transform data in your data warehouse.

It is a command line tool that uses a project structure to manage your code.

You can use SQL to deploy analytics code following software engineering best practices.

### How does it work?
turns the data into a model through a sql file. with dbt run, it will compile the code, select the raw data, transform and add it to the data warehouse.

dbt core is a open source tool to build a run dbt project, includes SQL compilation logic, macros anda database adapeters. Free to use.

dbt cloud is a hosted service that allows you to run dbt projects. It includes a web interface to manage your projects, teams, and collaboration. Its a web based IDE.

## Starting a dbt project

https://www.youtube.com/watch?v=J0XCDyKiU64&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=35&ab_channel=Victoria

alternative B, locally is: https://www.youtube.com/watch?v=1HmL63e-vRs&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=36&ab_channel=DataTalksClub%E2%AC%9B

every dbt project has many folders. dbt already will provide the starter project.
With the CLI, we can run dbt init.
with the dbt cloud, the IDE will guide us.

we will need the dbt_project.yml file to configure the project.

when configurint dbt, and adding github, the deploy key generated and added to github, give read and write permissions, without it, we can not commit the code from the dbt IDE.

## development of dbt models

https://www.youtube.com/watch?v=ueVy2N54lyc&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=37&ab_channel=Victoria

we will be using a modular data modeling.
First we have data tables that we loadedd, liket trip data, then we will build sql scripts tjhat we are going to call them models, in dbt that are going to be doing transformations.
So, we take the data, and with the models, we will clean, duplicate, recast, rename and son on.

we will alwaus work with sql files with the name of the model.
we will write a select statement, and then we will add the transformations that we want to do.
with config(materialized='table') we will specify that we want to create a table in the data warehouse.
we can also have view, incremental, ephemeral, etc.
- ephemeral models are temporary models that are not saved in the data warehouse. They only exist for a single dbt run.
- views are virtual tables created by dbt can be queries like regular tables.
- tables are saved in the data warehouse.
- incremetal materialization are a powerful feature that allows for efficient updates to existint rables reducing the need for full data refreshes.

the FROM clause:
Sources: configuration is in yaml files. Data loaded to our data warehouse that we uses a soruce for our models.
Seeds: csv files stores in our repository under seed folder. 
refs: macro to refrence the underlying tables and views that were building the data warehouse. Run the same code in any environment.

now, we created a schema.yml under models/staging. 

``` 
version: 2

sources:
  - name: staging
    database: dezoomcamp-ibai
    schema: trips_data_all
      
    tables:
      - name: green_tripdata
      - name: yellow_tripdata
```
Save and the generate the model green:

```
dbt run -m model_name
```
or also click on the model in dbt.
then, save the stg_green_tripdata.sql file.

then 
``` 
dbt build.
```
it wont work unless you create a new dataset in bigquery, unter EU with the dbt_dataset + name of the project: name: 'dbt_dataset_taxi_rides_ny_bq'

delete the examples because we will not use them.

I am in minute 17:28















