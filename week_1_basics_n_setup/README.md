
1.2.1 Introduction to Docker

LINK: https://www.youtube.com/watch?v=EYNwNlOrpr0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=4&ab_channel=DataTalksClub%E2%AC%9B

docker run -it --entrypoint=bash python:3.10 -> this will run the python image and open a bash shell

create a dockerfile and build the image:
docker build -t test:pandas . -> it will build the image in this directory

to run:
docker run -it test:pandas -> it will run the image

we can modify more the dockerfile and run it:

(base) ibai@ibai-PC:~/work/Data_Engineering_Zoomcamp/week_1_basics_n_setup/2_docker_sql$ docker run -it test:pandas 2021-01-15 123
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

now, in pgAdmin, when creating a server, we can select the network pg-network as host name.