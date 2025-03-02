
## homework.

step by step:

1. Create a new project 
2. Create a new bucket
3. Create a new service account. Give Storage admin privileges
4. Create a new key and get the credentials of the service account. 
5. add the credentials to the python script. We can also add them with External variables. 
6. After uploading the data, go to bigquery and create a dataset
7. Now, create an external table:
    CREATE OR REPLACE EXTERNAL TABLE `dezoomcamp-ibai.yellow_taxi_2024_1_6.yellow_taxi_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://dezoomcamp_bigquery_week3_2025/yellow_tripdata_*.parquet']
);

8. from this external table, we can create a  regular table:
    CREATE OR REPLACE TABLE `dezoomcamp-ibai.yellow_taxi_2024_1_6.yellow_taxi`
AS
SELECT * FROM `dezoomcamp-ibai.yellow_taxi_2024_1_6.yellow_taxi_external`;


## Question 1:
Question 1: What is count of records for the 2024 Yellow Taxi Data?
- 65,623
- 840,402
- 20,332,093   <- Number of rows
- 85,431,289


## Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.</br> 
What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?

- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- 0 MB for the External Table and 155.12 MB for the Materialized Table   <- This one
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table

SELECT COUNT(DISTINCT(PULocationID)) FROM `dezoomcamp-ibai.yellow_taxi_2024_1_6.yellow_taxi`;
SELECT COUNT(DISTINCT(PULocationID)) FROM `dezoomcamp-ibai.yellow_taxi_2024_1_6.yellow_taxi_external`;


## Question 3:
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?
- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires 
reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.  <- this one
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, 
doubling the estimated bytes processed.
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed

SELECT PULocationID FROM `dezoomcamp-ibai.yellow_taxi_2024_1_6.yellow_taxi`
SELECT PULocationID, DOLocationID FROM `dezoomcamp-ibai.yellow_taxi_2024_1_6.yellow_taxi`

## Question 4:
How many records have a fare_amount of 0?
- 128,210
- 546,578
- 20,188,016
- 8,333 <- This

SELECT COUNT(1) FROM `dezoomcamp-ibai.yellow_taxi_2024_1_6.yellow_taxi`
WHERE fare_amount = 0;

## Question 5:
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)
- Partition by tpep_dropoff_datetime and Cluster on VendorID  <- This one
- Cluster on by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID

CREATE OR REPLACE TABLE `dezoomcamp-ibai.yellow_taxi_2024_1_6.yellow_taxi_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `dezoomcamp-ibai.yellow_taxi_2024_1_6.yellow_taxi_external`;

## Question 6:
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime
2024-03-01 and 2024-03-15 (inclusive)</br>

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values? </br>

Choose the answer which most closely matches.</br> 

- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table   <- This one
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table


## Question 7: 
Where is the data stored in the External Table you created?

- Big Query
- Container Registry
- GCP Bucket  <- this
- Big Table

## Question 8:
It is best practice in Big Query to always cluster your data:
- True
- False  <- not always, depends on dataset size


## (Bonus: Not worth points) Question 9:
No Points: Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

It says 0.  I guess it reads from the metadata? Because I removed the cached option.
SELECT COUNT(*) FROM `dezoomcamp-ibai.yellow_taxi_2024_1_6.yellow_taxi_partitioned_clustered`;


## Submitting the solutions

Form for submitting: https://courses.datatalks.club/de-zoomcamp-2025/homework/hw3