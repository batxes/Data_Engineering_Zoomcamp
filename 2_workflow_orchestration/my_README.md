# Workflow Orchestration

## 2.2.1 Intro 

https://www.youtube.com/watch?v=Np6QmmcgLCs&list=PLEK3H8YwZn1oPPShk2p5k3E9vO-gPnUCf&ab_channel=Kestra

We are gonna use Kestra for orchestration. It will help us with ETL and automating lots of processes. 
Kestra also lets you work with other languages. It also lets us monitor all worfklow and executions.
It also has lots of plugins.

This week we will build our own ETL pipeline: extract data and loat it to postgres and later into google cloud.
We will add then parameters to the execution for flexibility and schedule all this executions together with backfills in case something goes wrong. Finally We will install it in google cloud to have it into production and then sync the flows with git.

an example. 
we have 3 tasks: extract, transform and query.

the workflow has: id and namespace. Id is unique, name of the workflow, and namespace is like the folder where we will put the workdlow.

Later we have inputs. Calues we can pass at the start of aour workflow. 

Then, we have the tasks, in our case we will have 3. Ech of them with the id (extract as example), and each task will have uri, or type or scripts and other parameters.  

## 2.2.2 Learn Kestra

https://www.youtube.com/watch?v=o79n-EVpics&list=PLEK3H8YwZn1oPPShk2p5k3E9vO-gPnUCf&index=2&ab_channel=Kestra

# Hands-On Coding Project: Build Data Pipelines with Kestra

Copy the files and folders and run Kestra with docker compose

```bash
cd 02-workflow-orchestration/
docker compose up -d
```

## 2.2.3 Creata an ETL pipeline with Postgres in Kestra

https://www.youtube.com/watch?v=OkfLX28Ecjg&list=PLEK3H8YwZn1oPPShk2p5k3E9vO-gPnUCf&index=3&ab_channel=Kestra

We have NY taxi yellow dataset and create a pipeline with Kestra to add it to the database.

we will create a pipeline to add data monthly, since we are getting this data monthly.

First, we will extract the data:
We have the name space and the inputs, with the values we can select and defaults.


id: 02_postgres_taxi
namespace: zoomcamp
description: |
  The CSV Data used in the course: https://github.com/DataTalksClub/nyc-tlc-data/releases

inputs:
  - id: taxi
    type: SELECT
    displayName: Select taxi type
    values: [yellow, green]
    defaults: yellow

  - id: year
    type: SELECT
    displayName: Select year
    values: ["2019", "2020"]
    defaults: "2019"

  - id: month
    type: SELECT
    displayName: Select month
    values: ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    defaults: "01"

Now here we have the variables so that we can dynamically operate:

variables:
  file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
  staging_table: "public.{{inputs.taxi}}_tripdata_staging"
  table: "public.{{inputs.taxi}}_tripdata"
  data: "{{outputs.extract.outputFiles[inputs.taxi ~ '_tripdata_' ~ inputs.year ~ '-' ~ inputs.month ~ '.csv']}}"

staging table is the monthly data, and table is ALL the data, which will be in data itself.

and here come the tasks to do:

tasks:
  - id: set_label
    type: io.kestra.plugin.core.execution.Labels
    labels:
      file: "{{render(vars.file)}}"
      taxi: "{{inputs.taxi}}"

  - id: extract
    type: io.kestra.plugin.scripts.shell.Commands
    outputFiles:
      - "*.csv"
    taskRunner:
      type: io.kestra.plugin.core.runner.Process
    commands:
      - wget -qO- https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{{inputs.taxi}}/{{render(vars.file)}}.gz | gunzip > {{render(vars.file)}}

This does not work unless we create the database.
with docker compose up, we already have it running.

Next, we have another task which is from postgresql.Queries, and creates a table and so on.

When we see render, means that the expresison inside needs to be "executed" because it is perse a variable. SO first that gets executed and becomes a string and then we can use the variable.

For the kestra and postgres to connect together, in the flows, I had to add this:

pluginDefaults:
  - type: io.kestra.plugin.jdbc.postgresql
    values:
      url: jdbc:postgresql://postgres:5432/postgres
      username: kestra
      password: k3str4

## 2.2.4 Manage Scheduling and Backfills with Postgres in Kestra

https://www.youtube.com/watch?v=_-li_z97zog&list=PLEK3H8YwZn1oPPShk2p5k3E9vO-gPnUCf&index=4&ab_channel=Kestra

We will use triggers to automatically add data to the DB


triggers:
  - id: green_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 1 * *"
    inputs:
      taxi: green

  - id: yellow_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 10 1 * *"
    inputs:
      taxi: yellow

But to fill data from the past, we need to do backfills. 

We can do that going to triggers -> backfill executions and go to 2019.

## 2.2.5 Orchestrate dbt Models with Postgres in Kestra

https://www.youtube.com/watch?v=ZLp2N6p2JjE&list=PLEK3H8YwZn1oPPShk2p5k3E9vO-gPnUCf&index=5&ab_channel=Kestra

IN the flow for dbt, we will pull from a folder and get the dbt code and files and run it in kestra. (the code will be known on week 4)

# ETL Pipelines in Kestra: Google Cloud Platform

## 2.2.6 - Create an ETL Pipeline with GCS and BigQuery in Kestra

https://www.youtube.com/watch?v=nKqjjLJ7YXs&list=PLEK3H8YwZn1oPPShk2p5k3E9vO-gPnUCf&index=6&ab_channel=Kestra

First, we need to configure google cloud with service account, project id, different names for the bucket, service names and so on.
In kestra, we have key-value pairs, to use it, like environment variables.
First go to google cloud and create a project: kestra-zoomcamp
Then Menu -> IAM -> service account -> create service account -> Name zoomcamp -> roles: storage admin, bigquery admin (we can give total Admin but only to learn) -> service account admin role: my email
now click on the service account -> key -> create json key (THIS IS THE GCP_CREDS).

Now, we can take the json, save it, and copy all from inside into Kestra key-value. I named GCP_CREDS

now, we add this flow:

id: 04_gcp_kv
namespace: zoomcamp

tasks:
  - id: gcp_project_id
    type: io.kestra.plugin.core.kv.Set
    key: GCP_PROJECT_ID
    kvType: STRING
    value: kestra-zoomcamp # TODO replace with your project id

  - id: gcp_location
    type: io.kestra.plugin.core.kv.Set
    key: GCP_LOCATION
    kvType: STRING
    value: europe-west2

  - id: gcp_bucket_name
    type: io.kestra.plugin.core.kv.Set
    key: GCP_BUCKET_NAME
    kvType: STRING
    value: kestra-de-zoomcamp-bucket-ibai # TODO make sure it's globally unique!

  - id: gcp_dataset
    type: io.kestra.plugin.core.kv.Set
    key: GCP_DATASET
    kvType: STRING
    value: zoomcamp

if we run this, in kestra -> namespace -> zoomcamp we will have the KEYS

Now, we go to gcp_setup flow. Here we will create the bucket and bigquery dataset.
We can see them created in the GCP

Google cloud storage is a data lake, and is used for object storage, like unstractured objects. But we can also store csv files that we can then use in bigquery, which is a data warehouse, which is used for storing structured data. SO the csv file can be put into a table and manipulate. That is  why we will use data lake to store the original source data and then send it to bigquery to then process and dig in.

Lets begin now with the gcp_taxi flow. Execute and see how we now have uploaded the csv to GCS. 
We are ready to use it and pass it to bigquery. let's add a table with bigquery. (we are doing that in the same flow)
We can see in GCP bigquery, how we created the table.
The idea now is to send the csv file to bigquery, add unique id and filename in bigquery, and then merge the table to create the big table with all the data.


## 2.2.7 - Manage Scheduling and Backfills using BigQuery in Kestra

https://www.youtube.com/watch?v=DoaZ5JWEkH0&list=PLEK3H8YwZn1oPPShk2p5k3E9vO-gPnUCf&index=7&ab_channel=Kestra

How can we schedule workflows and do backills?
for scheduling flows we use triggers.

backfills directly from the web

## 2.2.8 - Transform Data with dbt and BigQuery in Kestra

https://www.youtube.com/watch?v=eF_EdV4A1Wk&list=PLEK3H8YwZn1oPPShk2p5k3E9vO-gPnUCf&index=8&ab_channel=Kestra

Here we have a workflow in kestra that uses dbt to get the data modify it and put it back in bigquery

## 2.2.9 - Deploy Workflows to the Cloud with Git in Kestra

https://www.youtube.com/watch?v=l-wC71tI3co&list=PLEK3H8YwZn1oPPShk2p5k3E9vO-gPnUCf&index=9&ab_channel=Kestra


