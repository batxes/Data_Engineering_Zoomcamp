
1.2.1 Introduction to Docker

LINK: https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=4&ab_channel=DataTalksClub%E2%AC%9B

docker run -it --entrypoint=bash python:3.10 -> this will run the python image and open a bash shell

create a dockerfile and build the image:
docker build -t test:pandas . -> it will build the image in this directory

to run:
docker run -it test:pandas -> it will run the image

we can modify more the dockerfile and run it:

(base) ibai@ibai-PC:~/work/Data_Engineering_Zoomcamp/1_docker_terraform/2_docker_sql$ docker run -it test:pandas 2021-01-15 123
['pipeline.py', '2021-01-15', '123']
job finished successfully for day = 2021-01-15

1.2.2, Ingesting Data to Postgres

LINK: https://www.youtube.com/watch?v=2JM-ziJt0WI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=5&ab_channel=DataTalksClub%E2%AC%9B

Run postgres: with docker

docker run -it \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=ny_taxi \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13

  
if you get this error:

docker: Error response from daemon: driver failed programming external connectivity on endpoint awesome_chatelet (350bfc7693dc36f483a2f5e41c2222d74502c99661b957af1e5b44a991183eed): Error starting userland proxy: listen tcp4 0.0.0.0:5432: bind: address already in use.

sudo service postgresql stop

- another problem:
    if you can not open the ny_taxi_postgres_data folder, is because permissions where changed.
    sudo chown -R ibai:ibai ny_taxi_postgres_data/


Now, run CLi client:
pgcli

pip install pgcli

pgcli -h localhost -p 5432 -u root -d ny_taxi

root, root

 we can do now: \dt, selecf 1; 

now we will take the dataset and load to the postgres database. Let's run jupyter notebook.


1.2.3, connecting PGadmin with Postgres

LINK: https://www.youtube.com/watch?v=hCAIVe9N0ow&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=7&ab_channel=DataTalksClub%E2%AC%9B

SELECT count(1) FROM yellow_taxi_data;

SELECT max(tpep_pickup_datetime), min(tpep_pickup_datetime), max(total_amount) FROM yellow_taxi_data;

this is not very convenient, so we will use pgadmin to connect to the postgres database.
https://www.pgadmin.org/download/pgadmin-4-container/


docker run -it \
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
  -e PGADMIN_DEFAULT_PASSWORD=root \
  -p 8080:80 \
  -d dpage/pgadmin4:latest

go to http://localhost:8080/browser/

here we create a server and try to connect to localhost:5432, but it will fail, because localhost is because we are running the pgadmin in docker, and the postgres is running in another container.

We need to link the pgadmin with the postgres container, we can put them together in the same network.

so, stop both containers. 
docker stop <container_id>
docker rm <container_id>

now we do:
docker network create pg-network

docker run -it \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=root \
  -e POSTGRES_DB=ny_taxi \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13


docker run -it \
  -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
  -e PGADMIN_DEFAULT_PASSWORD=root \
  -p 8080:80 \
  --network=pg-network \
  --name pg-admin \
  dpage/pgadmin4

now, in pgAdmin, when creating a server, we can select the network pg-database as host name. (it will fine the name of the postgres container)

1.2.4, Dockerizing the ingestion pipeline
LINK: https://www.youtube.com/watch?v=B1WwATwf-vY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=8&ab_channel=DataTalksClub%E2%AC%9B

I will turn the notebook into script, and put the code in the pipeline.py file.

first: jupyter nbconvert --to=script eda.ipynb

add some code to the file, like argparse to pass the parameters.

now, in pgadmin, remove the table yellow_taxi_data:

DROP TABLE yellow_taxi_data;

now run: 

URL=https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_data \
  --url=${URL}

----- password should be in env variables


now that it works, we can create a docker image to run the pipeline. Modify the Dockerfile and build the image.

docker build -t taxi_ingest:v001 .

Now run it:

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_data \
    --url=${URL}

1.2.5  Running Postgres and pgAdmin with Docker-Compose

LINK: https://www.youtube.com/watch?v=hKI6PkPhpa0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=9&ab_channel=DataTalksClub%E2%AC%9B

we will use docker-compose to run the postgres and pgadmin, because it will be easier to manage the containers.
Services inside docker-compose.yaml are automatically in the same network, so we do not need to specify the network.

so, lets stop the containers and run docker-compose up.

docker-compose up

to stop, ctrl+c and then docker-compose down

1.2.6 - SQL Refreshser

LINK: https://www.youtube.com/watch?v=QEcps_iskgg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=10&ab_channel=DataTalksClub%E2%AC%9B

we will ingest the taxi zones data: https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv

I will add the code to do it in create_second_table_ingestion.py file.
Then, run this:

python create_second_table.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi 

check that we can access with localhost.


Different queries:

- joining tables (inner join)
SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough",' / ',zpu."Zone") AS "pickup_loc",
	CONCAT(zdo."Borough",' / ',zdo."Zone") AS "dropoff_loc"
FROM 
	yellow_taxi_data t, 
	zones zpu, 
	zones zdo
WHERE
	t."PULocationID" = zpu."LocationID" AND
	t."DOLocationID" = zdo."LocationID"
LIMIT 100;

This is the same as before, but with explicit inner join:

SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough",' / ',zpu."Zone") AS "pickup_loc",
	CONCAT(zdo."Borough",' / ',zdo."Zone") AS "dropoff_loc"
FROM 
	yellow_taxi_data t JOIN zones zpu
		ON t."PULocationID" = zpu."LocationID"
	JOIN zones zdo
		ON t."DOLocationID" = zdo."LocationID"
	
LIMIT 100;

- check if there is any null values:

SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM 
	yellow_taxi_data t 
WHERE
	"PULocationID" IS null

- check if there are any locations that are not in the zones table:

SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM 
	yellow_taxi_data t 
WHERE
	"PULocationID" NOT IN (SELECT "LocationID" FROM zones)

- delete smoe data

DELETE FROM zones WHERE "LocationID" = 142;

- and now, we will check outer join. Basically, we deleted 142, and we want when we execute the query above, to return for that location NULL or something similar. We use LEFT JOIN, means that if it is present in the left table, it will return the data, if not, it will return NULL.

SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough",' / ',zpu."Zone") AS "pickup_loc",
	CONCAT(zdo."Borough",' / ',zdo."Zone") AS "dropoff_loc"
FROM 
	yellow_taxi_data t LEFT JOIN zones zpu
		ON t."PULocationID" = zpu."LocationID"
	LEFT JOIN zones zdo
		ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;

- RIGHT JOIN: would be the same but for zones in this case. 

- OUTER JOIN, is a combination of LEFT JOIN and RIGHT JOIN: SHows records on the left when the are no records on the right, and vice versa.

- Here, we show DATE_TRUNC, which only shows days. We can also use CAST
SELECT 
	DATE_TRUNC('DAY', tpep_dropoff_datetime),
	total_amount
FROM 
	yellow_taxi_data 
LIMIT 100;

SELECT 
	CAST(tpep_dropoff_datetime AS DATE),
	total_amount
FROM 
	yellow_taxi_data 
LIMIT 100;

-using GROUP BY: Here we group all dates and count number of rows.

SELECT 
	CAST(tpep_dropoff_datetime AS DATE) as "day",
  COUNT(1) as "count"
FROM 
	yellow_taxi_data t
GROUP BY
  CAST(tpep_dropoff_datetime AS DATE)
ORDER BY "count" DESC;

- we can also add aggregations, like SUM, AVG, MIN, MAX, etc.

SELECT 
	CAST(tpep_dropoff_datetime AS DATE) as "day",
  COUNT(1) as "count",
  MAX (total_amount),
  MAX(passenger_count)
FROM 
	yellow_taxi_data t
GROUP BY
  CAST(tpep_dropoff_datetime AS DATE)
ORDER BY "count" DESC;

- TO GROUP BY MULTIPLE FIELDS

SELECT 
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	"DOLocationID",
  COUNT(1) as "count",
  MAX (total_amount),
  MAX(passenger_count)
FROM 
	yellow_taxi_data t
GROUP BY
  1, 2
ORDER BY "day" ASC, "DOLocationID" ASC;


1.3.1 - Terraform primer

LINK: https://www.youtube.com/watch?v=s2bOYDCKl_M&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12&ab_channel=DataSlinger

Terraform is a tool for building, changing, and versioning infrastructure safely and efficiently.Allows us to define the infrastructure as code and then apply it to the cloud provider.

Terraform is a declarative language, which means that we describe the desired state of the infrastructure, and Terraform will take care of creating and managing the infrastructure.

Key Terraform commands:

terraform init -> initialize the working directory
terraform plan -> plan the changes
terraform apply -> apply the changes
terraform destroy -> destroy the infrastructure

1.3.2 - Terraform Basics

LINK: https://www.youtube.com/watch?v=Y2ux7gq3Z0o&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12&ab_channel=DataSlinger

We will set up Terraform in GCP. For that we need a service account. Is like a user account but we won't login with it. It will be used by software to access the resources.

We will go to IAM and Admin -> service accounts -> create service account.
we will want cloud storage admin  and bigquery admin.
In the future, we would restrict the permissions a little bit, not give all permissions.

If in the future we want more roles, we can go to IAM -> edit -> add more roles.
We will also add Compute Admin.

Now, we will create a new key for the service account. Json.

Securely save the key in a safe place. I saved it in the keys folder, and added to gitignore, so I dont upload it to github.

Now, install in vscode the Terraform extension.
Create main.tf file in the 3_terraform folder.
search for  google coud platform provider: https://registry.terraform.io/providers/hashicorp/google/latest/docs 
and add it to the main.tf file.
add project and region to google provider. They are also in the linke above.

We can align the json with "terraform fmt".

Go to the GCP dashboard to grab the project id. 
Add also the credentials to the main.tf file. ANother way of authentication is using the gcloud cli. -> gcloud default auth-login -> gives us a link.

We can also do -> export GOOGLE_CREDENTIALS='/home/ibai/work/Data_Engineering_Zoomcamp/1_docker_terraform/3_terraform/keys/terraform_creds.json'


now, terraform init.

if successfully installed, it will create a .terraform folder and a .terraform lock.

Now lets create a bucket in google cloud. Visit this link: https://registry.terraform.io/providers/wiardvanrij/ipv4google/latest/docs/resources/storage_bucket

We add google storage bucket resource to the main.tf. Change resource variable and name. Name needs to be unique in whole google cloud, so we can add project name to it.

also change the time of action in the lifecycle.

Now, lets terraform plan.  We see what we will deploy later, and then -> terraform apply
WHen applying, it createss a tfstate file which shows  the resources. In the google cloud platform, check that the bucket appears

if we type terraform destroy, it would remove what we deployed.
It would create though a terraform.tfstate.backup

so remember:

terraform init
terraform plan
terraform apply
terraform destroy

1.3.3: Terraform Variables

go to google -> terraform bigquery dataset -> https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset

add the bigquery_Dataset block to main.tf

terraform apply ->  and chekc that demo_dataset was created in GCP.
then terraform destroy

Now we will create variable to use them in other files.
We will use them in the main.tf file here. Let's change all the names with the variables.

apply and destroy to see that it works.

lets also add the credentials as variable

1.4.1; Setting up the Environment on Google Cloud (Cloud VM + SSH access)

In GCP -> Compute Enginer -> VM instances

Before creating an instance, we need to generate an SSH key, the key that we will use to log in to the instance.
For that: https://cloud.google.com/compute/docs/connect/create-ssh-keys
go to .ssh directory in home
ssh-keygen -t rsa -f gcp -C ibai -b 2048
Enter
Enter (if we want we can add a password, but it will be needed every time we ssh to gcp)

Now, we will share the public key with GCP. Go to Compute enginer -> settings -> metadata -> SSH KEYS -> add the public key and save

Lets go now to VM instances and create an instance. Add name, region (I went with Belgium, it is cheapest), and E2 standard 4. 
We can also change to ubuntu, I choose 24.04 LTS, and 30 GB storage size. Create.
We need the external IP from the instance:

and we connect: ssh -i ~/.ssh/gcp ibai@35.195.229.234

We are inside:

ibai@de-zoomcamp:~$ gcloud --version
Google Cloud SDK 506.0.0
alpha 2025.01.10
beta 2025.01.10
bq 2.1.11
bundled-python3-unix 3.11.9
core 2025.01.10
gcloud-crc32c 1.0.0
gsutil 5.33
minikube 1.34.0
skaffold 2.13.1

First thing, we will download Anaconda. wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
and install it: bash Anaconda3-2024.10-1-Linux-x86_64.sh
allow to change the PATH so that we can call conda, if not, it will be in anaconda3/condabin/conda

now, we will create a config file in .ssh to the connect easily to the gcp VM instance.
add this to the config:

Host de-zoomcamp
    HostName 35.195.229.234
    User ibai
    IdentityFile ~/.ssh/gcp       

and then ssh de-zoomcamp

now install docker: 
sudo apt-get update
sudo apt-get install docker.io

now we want to access the virtual machine from vscode. for that, go to extensions and install "remote ssh" (in cursor is installed) -> click left bottom corner, then connect host -> and we will have de-zoomcamp already there. (from the previous config file)

It opens another vscode window. Lets clone the code repo to the VM in the terminal.
We now test docker, but it needs permissions: check this: 
https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md
basically do:
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo service docker restart
reconnect to the VM

now we want to install docker compose: Go to github and copy the latest release: https://github.com/docker/compose
https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-x86_64
create the directory /bin and run inside: 
  wget https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-x86_64 -O docker-compose

make it exex: chmod +x docker-compose
to make it visible from any dir add to PATH variable in bashrc:
 export PATH="${HOME}"/bin:${PATH}
 source .bashrc

now lets run docker-compose in the data-engineering dir:
  ibai@de-zoomcamp:~/data-engineering-zoomcamp/01-docker-terraform/2_docker_sql$ docker-compose up -d

  it will download postgresql and pgadmin images and they will start running.
  docker ps

now install pgcli: pip install pgcli (if this fail, we can install it with conda)

connect: pgcli -h localhost -U root -d ny_taxi
pass is root

now, to access this postgres database, which is running in the port 5432 in the VM, we need to forward the port to our local machine.
Go to VScode. control + ` -> ports -> forward -> 5432.
now we can directly access the db from our computer: pgcli -h localhost -U root -d ny_taxi

  PROBLEM: 
  (base) ibai@ibai-PC:~$ pgcli -h 127.0.0.1 -U root -d ny_taxi
  Password for root: 
  connection failed: connection to server at "127.0.0.1", port 5432 failed: FATAL:  password authentication failed for user "root"
  connection to server at "127.0.0.1", port 5432 failed: FATAL:  password authentication failed for user "root"

  check that the port was properly forwarded. If 5432 is being used, kill the process:
  sudo lsof -i :5432
  sudo kill -9 PID

Now we want to add data to the db
We first want to forward 8080 for pgadmin, use again vscode. admin@admin -> pass:root
forward 8888 for jupyter notebook and then run to upload data to the db in the VM.
First download the data, because we do not ahve it in the VM: 
  wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
  note: modify the read_csv and alsoo add this line to the notebook: !pip install psycopg2-binary
  then connect, create table and insert first 100.
  Check: select count(1) from yellow_taxi_data;

Now, lets install terraform. DOwnload in the bin dir and unzip: 
wget https://releases.hashicorp.com/terraform/1.10.5/terraform_1.10.5_linux_amd64.zip  
unzip terraform_1.10.5_linux_amd64.zip

it is already executable and in bin folder so we can call it from anywhere
We will set up terraform now: plan, apply and so on.
We need the service account json credentials. We will put the json file in the VM, with sftp.
sftp de-zoomcamp
Connected to de-zoomcamp.
sftp> mkdir .gc
sftp> cd .gc
sftp> ls
sftp> put terraform_creds.json
Uploading terraform_creds.json to /home/ibai/.gc/terraform_creds.json
terraform_creds.json                     100% 2395    97.3KB/s   00:00    
sftp> 

Now, to authonticate in the VM:
  export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/terraform_creds.json
  gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

  now, in the VM, we can go and do the init, plan and apply.

Tu shutdown the VM:
  in GCP, actions->stop (also delete) / delete will remove everything, data too. (I will be charged for the storage if not deleted.)
  or "shutdown now" from the terminal
WHen restarting, the IP might change so we have to also change the .ssh/config file



































