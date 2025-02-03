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


## 2.2.4 Manage Scheduling and Backfills with Postgres in Kestra

https://www.youtube.com/watch?v=_-li_z97zog&list=PLEK3H8YwZn1oPPShk2p5k3E9vO-gPnUCf&index=4&ab_channel=Kestra




