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

