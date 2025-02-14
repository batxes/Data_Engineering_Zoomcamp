
# Video notes

## Data ingestion with dlt

https://www.youtube.com/live/pgJWP_xqO1g


dlt hub = open source library. data load tool

Data ingestion steps (ETL) are

extract, transform and load

In the extraction, normally we will get the data from SQL dbs, Files or APIs

and between APIs, we can have:
RESTfulAPIs, FIle based APIS and Database APIS

RESTful APIs are the most common. They allow structured data extraction using HTTPS requests (GET, POST, PUT, DELETE).
It is the mosto common, but each of them is most of the times unique and can be challenging.

an example:
```py
    import requests

    result = requests.get("https://api.github.com/orgs/dlt-hub/repos").json()
    print(result[:2])
```

Challenges:

We need to pay attention to rate limits, pagination, authentication and memory limits.

Rate limits: many put a limit to prevent overloading. SO we need to monitor these limits, pause requests if needed and implement automatic retries.
Authentication: Many APIs require API key or token. Types ot Authnetication are: API keys, OAuthg Tokens and basic authnetication using username and password. Put this tokens in environment or some places like Secretes in Colab.
Pagination: Many APIs regurn data in chunks or pages. To retrieve everything we need to iterate. 
EXAMPLE:
```py
    import requests

    BASE_API_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

    page_number = 1
    while True:
        params = {'page': page_number}
        response = requests.get(BASE_API_URL, params=params)
        page_data = response.json()

        if not page_data:
            break

        print(page_data)
        page_number += 1

        # limit the number of pages for testing
        if page_number > 2:
        break
```

Avoiding memory issues during extraction: You dont want load everything in memory. This happens because our extraction may be in a serverless or cluster and the data will be stored in memory. Solution is to batch processing/streaming data. This means processing data in small chunks, instead of doing all at once.
EXMAPLE:
```py
    import requests

    BASE_API_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

    def paginated_getter():
        page_number = 1
        while True:
            params = {'page': page_number}
            try:
                response = requests.get(BASE_API_URL, params=params)
                response.raise_for_status()
                page_json = response.json()
                print(f'Got page {page_number} with {len(page_json)} records')

                if page_json:
                    yield page_json
                    page_number += 1
                else:
                    break
            except Exception as e:
                print(e)
                break


    for page_data in paginated_getter():
        print(page_data)
        break
```

To simplify data extraction we can use tools like dlt. Dlt simplifies the process of pagination, rate limits, authentication and errors with a buil-in REST API Client, making extraction efficient, scalable and reliable.

```
pip install dlt[duckdb]
```

we put duckdb so we install dlt where we only want to load the data into duckdb. duckdb is a lightweight database, easy to work. It could be bigqyer, postgersql or whatveer we want.


Instead of manually writing pagination logic, let’s use **dlt’s [`RESTClient` helper](https://dlthub.com/docs/general-usage/http/rest-client)** to extract NYC taxi ride data:  
```py
import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


def paginated_getter():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        # Define pagination strategy - page-based pagination
        paginator=PageNumberPaginator(   # <--- Pages are numbered (1, 2, 3, ...)
            base_page=1,   # <--- Start from page 1
            total_path=None    # <--- No total count of pages provided by API, pagination should stop when a page contains no result items
        )
    )

    for page in client.paginate("data_engineering_zoomcamp_api"):    # <--- API endpoint for retrieving taxi ride data
        yield page   # remember about memory management and yield data

for page_data in paginated_getter():
    print(page_data)
```

**How dlt simplifies API extraction:**  

🔹 **No manual pagination** – dlt **automatically** fetches **all pages** of data.  
🔹 **Low memory usage** – Streams data **chunk by chunk**, avoiding RAM overflows.  
🔹 **Handles rate limits & retries** – Ensures requests are sent efficiently **without failures**.  
🔹 **Flexible destination support** – Load extracted data into **databases, warehouses, or data lakes**.



Now, next step, normalize the data.

normally we have 2 steps, normalizing and filtering for a specific use case.

Normalizing (cleaning, transformation): we perform several tasks:
    add types
    rename columns
    flatten nested dictionaries
    unnest list/arrays

dlt already automatically normalizes. the data gets unested, datatype changes and more. an example:


```py
data = [
    {
        "vendor_name": "VTS",
        "record_hash": "b00361a396177a9cb410ff61f20015ad",
        "time": {
            "pickup": "2009-06-14 23:23:00",
            "dropoff": "2009-06-14 23:48:00"
        },
        "coordinates": {
            "start": {"lon": -73.787442, "lat": 40.641525},
            "end": {"lon": -73.980072, "lat": 40.742963}
        },
        "passengers": [
            {"name": "John", "rating": 4.9},
            {"name": "Jack", "rating": 3.9}
        ]
    }
]
```


```py
import dlt

# Define a dlt pipeline with automatic normalization
pipeline = dlt.pipeline(
    pipeline_name="ny_taxi_data",
    destination="duckdb",
    dataset_name="taxi_rides",
)

# Run the pipeline with raw nested data
info = pipeline.run(data, table_name="rides", write_disposition="replace")

# Print the load summary
print(info)

print(pipeline.last_trace)
```

in this example, columns were unnested. It takes the names from the json for example, and creates the name of the columns with the underscores.
It also creates another child table, in this case for the passangers, with name, rating and ids.
It also added ID's to the track.


now, lets starrt loading data.


### **Why use dlt for loading?**  

✅ **Supports multiple destinations** – Load data into **BigQuery, Redshift, Snowflake, Postgres, DuckDB, Parquet (S3, GCS)** and more.  
✅ **Optimized for performance** – Uses **batch loading, parallelism, and streaming** for fast and scalable data transfer.  
✅ **Schema-aware** – Ensures that **column names, data types, and structures match** the destination’s requirements.  
✅ **Incremental loading** – Avoids unnecessary reloading by **only inserting new or updated records**.  
✅ **Resilience & retries** – Automatically handles failures, ensuring data is loaded **without missing records**.

example:


```py
import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


# Define the API resource for NYC taxi data
@dlt.resource(name="rides")   # <--- The name of the resource (will be used as the table name)
def ny_taxi():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None
        )
    )

    for page in client.paginate("data_engineering_zoomcamp_api"):    # <--- API endpoint for retrieving taxi ride data
        yield page   # <--- yield data to manage memory


# define new dlt pipeline
pipeline = dlt.pipeline(destination="duckdb")

# run the pipeline with the new resource
load_info = pipeline.run(ny_taxi, write_disposition="replace")
print(load_info)

# explore loaded data
pipeline.dataset(dataset_type="default").rides.df()
```


Incremental loading is when we want to just load a new record, not all again.
there are 2 key concepts here:
- **Incremental extraction** – Only extracts the new or modified data rather than retrieving everything again.  
- **State tracking** – Keeps track of what has already been loaded, ensuring that only new data is processed.  

How does dlt do this?
2 ways:

#### **1. Append (adding new records)**  

- Best for **immutable or stateless data**, such as taxi ride records.  
- Each run **adds new records** without modifying previous data.  
- Can also be used to create a **history of changes** (slowly changing dimensions).  

**Example:**  
- If taxi ride data is loaded daily, only **new rides** are added, rather than reloading the full history.  
- If tracking changes in a list of vehicles, **each version** is stored as a new row for auditing.  

---

#### **2. Merge (updating existing records)**  

- Best for **updating existing records** (stateful data).  
- Replaces old records with updated ones based on a **unique key**.  
- Useful for tracking **status changes**, such as payment updates.  

**Example:**  
- A taxi ride's **payment status** could change from `"booked"` to `"cancelled"`, requiring an update.  
- A **customer profile** might be updated with a new email or phone number.  

we need to add this line:
```python
cursor_date = dlt.sources.incremental("Trip_Dropoff_DateTime", initial_value="2009-06-15")
```

EXAMPLE:


```py
import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


@dlt.resource(name="rides", write_disposition="append")
def ny_taxi(
    cursor_date=dlt.sources.incremental(
        "Trip_Dropoff_DateTime",   # <--- field to track, our timestamp
        initial_value="2009-06-15",   # <--- start date June 15, 2009
        )
    ):
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None
        )
    )

    for page in client.paginate("data_engineering_zoomcamp_api"):
        yield page
```

Finally, we run our pipeline and load the fresh taxi rides data:

```py
# define new dlt pipeline
pipeline = dlt.pipeline(pipeline_name="ny_taxi", destination="duckdb", dataset_name="ny_taxi_data")

# run the pipeline with the new resource
load_info = pipeline.run(ny_taxi)
print(pipeline.last_trace)
```

Only 5325 rows were flitered out and loaded into the `duckdb` destination. Let's take a look at the earliest date in the loaded data:

```py
with pipeline.sql_client() as client:
    res = client.execute_sql(
            """
            SELECT
            MIN(trip_dropoff_date_time)
            FROM rides;
            """
        )
    print(res)
```

Run the same pipeline again.

```py
# define new dlt pipeline
pipeline = dlt.pipeline(pipeline_name="ny_taxi", destination="duckdb", dataset_name="ny_taxi_data")


# run the pipeline with the new resource
load_info = pipeline.run(ny_taxi)
print(pipeline.last_trace)
```

The pipeline will detect that there are **no new records** based on the `Trip_Dropoff_DateTime` field and the incremental cursor. As a result, **no new data will be loaded** into the destination:
>0 load package(s) were loaded


## more stuff

### **Example: Loading data into a Data Warehouse (BigQuery)**  
First, install the dependencies, define the source, then change the destination name and run the pipeline.

```shell
pip install dlt[bigquery]
```

Let's use our NY Taxi API and load data from the source into destination.

```py
import dlt
from dlt.sources.helpers.rest_client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator


@dlt.resource(name="rides", write_disposition="replace")
def ny_taxi():
    client = RESTClient(
        base_url="https://us-central1-dlthub-analytics.cloudfunctions.net",
        paginator=PageNumberPaginator(
            base_page=1,
            total_path=None
        )
    )

    for page in client.paginate("data_engineering_zoomcamp_api"):
        yield page
```


**Choosing a destination**

Switching between  **data warehouses (BigQuery, Snowflake, Redshift)** or **data lakes (S3, Google Cloud Storage, Parquet files)**  in dlt is incredibly straightforward — simply modify the `destination` parameter in your pipeline configuration. 

For example:

```py
pipeline = dlt.pipeline(
    pipeline_name='taxi_data',
    destination='duckdb', # <--- to test pipeline locally
    dataset_name='taxi_rides',
)

pipeline = dlt.pipeline(
    pipeline_name='taxi_data',
    destination='bigquery', # <--- to run pipeline in production
    dataset_name='taxi_rides',
)
```

This flexibility allows you to easily transition from local development to production-grade environments.

> 💡 No need to rewrite your pipeline — dlt adapts automatically!

**Set Credentials**  

The next logical step is to [set credentials](https://dlthub.com/docs/general-usage/credentials/) using **dlt's TOML providers** or **environment variables (ENVs)**.

```py
import os
from google.colab import userdata

os.environ["DESTINATION__BIGQUERY__CREDENTIALS"] = userdata.get('BIGQUERY_CREDENTIALS')
```

Run the pipeline:
```py
pipeline = dlt.pipeline(
    pipeline_name="taxi_data",
    destination="bigquery",
    dataset_name="taxi_rides",
    dev_mode=True,
)

info = pipeline.run(ny_taxi)
print(info)
```

💡 **What’s different?**  
- **dlt automatically adapts the schema** to fit BigQuery.  
- **Partitioning & clustering** can be applied for performance optimization.  
- **Efficient batch loading** ensures scalability.

---

### **Example: Loading data into a Data Lake (Parquet on Local FS or S3)**  

**Why use a Data Lake?**  
- **Cost-effective storage** – Cheaper than traditional databases.   
- **Optimized for big data processing** – Works seamlessly with Spark, Databricks, and Presto.  
- **Easy scalability** – Store petabytes of data efficiently.  


The `filesystem` destination enables you to load data into **files stored locally** or in **cloud storage** solutions, making it an excellent choice for lightweight testing, prototyping, or file-based workflows.

Below is an **example** demonstrating how to use the `filesystem` destination to load data in **Parquet** format:

* Step 1: Set up a local bucket or cloud directory for storing files

```py
import os

os.environ["BUCKET_URL"] = "/content"
```

* Step 2: Define the data source (above)
* Step 3: Run the pipeline

```py
import dlt


pipeline = dlt.pipeline(
    pipeline_name='fs_pipeline',
    destination='filesystem', # <--- change destination to 'filesystem'
    dataset_name='fs_data',
)

load_info = pipeline.run(ny_taxi, loader_file_format="parquet") # <--- choose a file format: parquet, csv or jsonl
print(load_info)
```

Look at the files:

```shell
! ls fs_data/rides
```

Look at the loaded data:

```py
# explore loaded data
pipeline.dataset(dataset_type="default").rides.df()
```

#### **Table formats: [Delta tables & Iceberg](https://dlthub.com/docs/dlt-ecosystem/destinations/delta-iceberg)**
these are different kind of table formats which add layers of metadata.

dlt supports writing **Delta** and **Iceberg** tables when using the `filesystem` destination.

**How it works:**

dlt uses the `deltalake` and `pyiceberg` libraries to write Delta and Iceberg tables, respectively. One or multiple Parquet files are prepared during the extract and normalize steps. In the load step, these Parquet files are exposed as an Arrow data structure and fed into `deltalake` or `pyiceberg`.

```shell
 !pip install "dlt[pyiceberg]"
```

```py
pipeline = dlt.pipeline(
    pipeline_name='fs_pipeline',
    destination='filesystem', # <--- change destination to 'filesystem'
    dataset_name='fs_iceberg_data',
)

load_info = pipeline.run(
    ny_taxi,
    loader_file_format="parquet",
    table_format="iceberg",  # <--- choose a table format: delta or iceberg
)
print(load_info)
```








