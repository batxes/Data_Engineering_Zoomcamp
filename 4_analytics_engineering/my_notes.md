
# Analytics Engineering

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

every dbt project has many folders. dbt already will provide the starter project.
With the CLI, we can run dbt init.
with the dbt cloud, the IDE will guide us.

we will need the dbt_project.yml file to configure the project.









