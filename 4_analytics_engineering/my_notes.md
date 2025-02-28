
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

Now lets learn about Macros:

Those are the curly brackets: { }
It actually uses jinja templating language.
We will call functions inside those brackets.
they have input and the output is code.
It will also help us create our own functions and code, dynamically.
between {% %} we will write the code. it will be executed and get a variable in between {{}}

We will create a macro in dbt: macros folder-> create a file -> get_payment_type_description.sql

```
{#
    This macro returns the description of the payment_type 
#}

{% macro get_payment_type_description(payment_type) -%}

    case {{ dbt.safe_cast("payment_type", api.Column.translate_type("integer")) }}  
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Unknown'
        when 6 then 'Voided trip'
        else 'EMPTY'
    end

{%- endmacro %}
```

payment_type then can be used anywhere in the project.

add to the select clause in stg_green_tripdata.sql:

```
{{ get_payment_type_description(payment_type) }} as payment_type_description
```
compile and see what the macro does.

We can also write packages. These are dbt projects that can be reused in other projects.
Like libraries in other programming languages.
imported in the packages.yml file and imported by running dbt deps.
dbt_packages_hub.com is a website that has a lot of packages.

we will use dbt_utils. Copy how we install it.
```
packages:
  - package: dbt-labs/dbt_utils
    version: 1.3.0
```

create packages.yml under the home of dbt project and paste that code.
now, dbt deps will install the package.

now copy the code for generate_surrogate_key.sql and paste it in the macros folder (from the dbt uitls, in the hub webpase).

```
{{ dbt_utils.generate_surrogate_key(['field_a', 'field_b'[,...]]) }}
```

we will add to stg_green_tripdata.sql:

```
{{ dbt_utils.generate_surrogate_key(['VendorID', 'lpep_pickup_datetime']) }} as trip_id
```

let's build the stg_green_tripdata model.

everytime we run dbt build, bigquery will be updated.

Now, we are ready to copy the whole code fromt eh respository of data talks club.
https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/taxi_rides_ny/models/staging/stg_green_tripdata.sql

in this code, 
we have a config macro. It is not needed really but it does not hurt. 
we can get the code with underscore underscore. __ and then tab, to open autocomplete jinja.

then, there is lots of code and in the end, variables:

Variables are useful for defining parameters that can be reused in the code.

```
{{ var('my_var') }}
``` 

regardles, lets run the code as it is. 
dbt build

I actually get an error, because the table in bigquery contains a float in a column and dbt can not partition with float.

Regardles, lets continue.
In the code, we can build with a variable:

if we want to change the limit in the sql model, we can do this:

-- dbt build --select stg_green_tripdata --vars '{'is_test_run': 'false'}'

now, it will not add the limit 100

now, create a file in staging: stg_yellow_tripdata.sql
and copy the code from the repository.


now add seeds.
the link is here: https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/taxi_rides_ny/seeds/taxi_zone_lookup.csv
go to raw, and copy. 
under seeds, create a file, taxi_zone_lookup.csv and paste the data.
build

if we do refresh in bigquery, we will see the data.


Now, in the models folder, craete a folder called core, and inside, dim_zones.sql file.
We will add all the information about the zones.
copy this code: https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/04-analytics-engineering/taxi_rides_ny/models/core/dim_zones.sql

this code is selecting from the taxi lookup table and selecting the borough, service zone, zone and the location id.

now create a fact_trips.sql model, under core folder.
fact_trips will combine in the end the green and yellow tripdata with the zone information.


## Testing and documenting dbt models
https://www.youtube.com/watch?v=2dNJXHFCHaY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=38&ab_channel=Victoria

dbt tests

assumptions that we make about our data.
tests in dbt are essenelat a select sql query.
they return the amount of failing records
tests are defined on a colum in the .yml file.
dbt provides basic tests to check if the column values are unique, not null, accepted values and son on.

We can get also the package called dbt_codegen which generates code for us for different models.
It is also useful the dbt_expectations package, which contains lots of tests.


Documentation:
we can add real documentation to our models.
for every object that we have and use in dbt, will be able to create a web page with the documentation.
It will take infor from differnt places like the yml or our code

## Deployment of dbt project in the cloud

Deployment is the process of running the models we created in our development environment in a production environment.
A development -deployment workflow will be something like:
- develop in a user branch
- open a PR to merge into the main branch- merge the branch to themain brahnch
- run the new models in the production environment using the main branch
- schedule the models


Dbt cloud includes a scheduler where to create hobs to run in production.
A single job can run multiple commands
jobs can be triggered manually or scheduled
eachjob will keep a log of the returnsa job could also generate documanetation

We first go in the dbt cloud, to Deploy - > environments -> new one called production. Dataset = prod
Then, Create job -> Deploy job. Job name "nightly", Description = "This is where data hits production"
check Generate docs on the run.
Check run source freshness.
the command will be dbt build.
run on schedule and for example at 12h every day.

if we run manually, we will see that it first clones the repository, creates the bigquery connection, invokes dbt deps, dbt source freshnes, build and docs generate.

we can go to the dashboard, settings and check for nightly and go to the documentation.

Continuous Integration and Continuous deployment:
This is the practice of regularly merging code into main, and making sure that it is automated that is not going to break production, with tests and runs.

So we can create also a Continuous Integration job in dbt cloud, with production environment and triggered by pull requests.
the command will be dblt build --select state:modified+
we can also add another command like: dbt test documented_models
Compare everything against Production.

In case we want to do deplyment locally: https://www.youtube.com/watch?v=Cs9Od1pcrzM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=40&ab_channel=DataTalksClub%E2%AC%9B

## Visualizing data with Google Data Studio (alternative A)

https://www.youtube.com/watch?v=39nLTs74A3E&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=41&ab_channel=DataTalksClub%E2%AC%9B

go to google data studio: https://lookerstudio.google.com/u/0/navigation/reporting

create a data source -> big query and choose the dataset.

We then create a new report add the charts we want.
Later we can download the report as a dashboard or pdf.

## Visualizing data with Looker Studio (alternative B)

https://www.youtube.com/watch?v=39nLTs74A3E&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=41&ab_channel=DataTalksClub%E2%AC%9B


## Visualizing data with Metabase (alternative B)

https://www.youtube.com/watch?v=BnLkrA7a6gM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=42&ab_channel=DataTalksClub%E2%AC%9B




























