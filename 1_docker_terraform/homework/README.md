# Module 1 Homework: Docker & SQL

## Question 1. Understanding docker first run 

Run docker with the `python:3.12.8` image in an interactive mode, use the entrypoint `bash`.

What's the version of `pip` in the image?

- 24.3.1  X
- 24.2.1
- 23.3.1
- 23.2.1

(base) ibai@ibai-PC:~/work/Data_Engineering_Zoomcamp/week_1_basics_n_setup/homework$ docker run -it python:3.12.8 bash
(ALSO docker run -it --entrypoint=bash python:3.12.8)
root@57d15bad1693:/# pip --version
pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)

## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that **pgadmin** should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin  

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

- postgres:5433  
- localhost:5432
- db:5433
- postgres:5432  
- db:5432 X

If there are more than one answers, select only one of them

Hostname: db (because services within the same Docker network communicate using service names)
Port: 5432 (inside the container, PostgreSQL is running on its default internal port)

##  Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from October 2019:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz
```

You will also need the dataset with zones:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

Download this data and put it into Postgres.

You can use the code from the course. It's up to you whether
you want to use Jupyter or a python script.

what I did:

add both ingest_data.py and cread_second_table_ingestion.py files. CHange tpep_... for lpep...

URL=https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-10.parquet

python ingest_data.py \
  --user=postgres \
  --password=postgres \
  --host=localhost \
  --port=5433 \
  --db=ny_taxi \
  --table_name=green_taxi_data \
  --url=${URL}

python create_second_table_ingestion.py \
    --user=postgres \
    --password=postgres \
    --host=localhost \
    --port=5433 \
    --db=ny_taxi

Note: check that now host is localhost and port 5433, because we are doing it from our local machine

## Question 3. Trip Segmentation Count

During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, **respectively**, happened:
1. Up to 1 mile
2. In between 1 (exclusive) and 3 miles (inclusive),
3. In between 3 (exclusive) and 7 miles (inclusive),
4. In between 7 (exclusive) and 10 miles (inclusive),
5. Over 10 miles 

Answers:

- 104,802;  197,670;  110,612;  27,831;  35,281
- 104,802;  198,924;  109,603;  27,678;  35,189
- 104,793;  201,407;  110,612;  27,831;  35,281
- 104,793;  202,661;  109,603;  27,678;  35,189
- 104,838;  199,013;  109,645;  27,688;  35,202  X It is closest

I get: 104830, 198995, 109642, 27686, 35201



SELECT count(1)
FROM green_taxi_data 
WHERE lpep_pickup_datetime >= '2019-10-01' 
AND lpep_pickup_datetime < '2019-11-01'
AND trip_distance <= 1;

SELECT count(1)
FROM green_taxi_data 
WHERE lpep_pickup_datetime >= '2019-10-01' 
AND lpep_pickup_datetime < '2019-11-01'
AND trip_distance > 1
AND trip_distance <= 3;

...




## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance?
Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance. 

- 2019-10-11
- 2019-10-24
- 2019-10-26
- 2019-10-31  X

SELECT lpep_pickup_datetime, trip_distance
FROM green_taxi_data
WHERE trip_distance = (SELECT MAX(trip_distance) FROM green_taxi_data);


## Question 5. Three biggest pickup zones

Which were the top pickup locations with over 13,000 in
`total_amount` (across all trips) for 2019-10-18?

Consider only `lpep_pickup_datetime` when filtering by date.
 
- East Harlem North, East Harlem South, Morningside Heights <x>
- East Harlem North, Morningside Heights
- Morningside Heights, Astoria Park, East Harlem South
- Bedford, East Harlem North, Astoria Park

SELECT 
    z."Zone" AS pickup_location, 
    t."PULocationID", 
    SUM(total_amount) AS total_revenue
FROM green_taxi_data t
JOIN zones z ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2019-10-18'
GROUP BY t."PULocationID", z."Zone"
HAVING SUM(total_amount) > 13000
ORDER BY total_revenue DESC;

## Question 6. Largest tip

For the passengers picked up in October 2019 in the zone
named "East Harlem North" which was the drop off zone that had
the largest tip?

Note: it's `tip` , not `trip`

We need the name of the zone, not the ID.

- Yorkville West
- JFK Airport  X 
- East Harlem North
- East Harlem South

SELECT 
    dropoff_zone."Zone" AS dropoff_location,
    MAX(t.tip_amount) AS max_tip
FROM green_taxi_data t
JOIN zones pickup_zone ON t."PULocationID" = pickup_zone."LocationID"
JOIN zones dropoff_zone ON t."DOLocationID" = dropoff_zone."LocationID"
WHERE pickup_zone."Zone" = 'East Harlem North'
AND t.lpep_pickup_datetime >= '2019-10-01' 
AND t.lpep_pickup_datetime < '2019-11-01'
GROUP BY dropoff_zone."Zone"
ORDER BY max_tip DESC
LIMIT 1;


## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](../../../01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Terraform Workflow

Which of the following sequences, **respectively**, describes the workflow for: 
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

Answers:
- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- terraform init, terraform apply -auto-approve, terraform destroy  X
- terraform import, terraform apply -y, terraform rm


## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2025/homework/hw1