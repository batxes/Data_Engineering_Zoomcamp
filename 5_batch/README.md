# Module 5: Batch Processing

## 5.1 Introduction

* :movie_camera: 5.1.1 Introduction to Batch Processing

[![](https://markdown-videos-api.jorgenkh.no/youtube/dcHe5Fl3MF8)](https://youtu.be/dcHe5Fl3MF8&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=51)

Many ways of processing data.
Batch and streaming.

Batch processing is when the processing and analysis happens on a set of data that have already been stored over a period of time
Streaming data processing happens as the data flows through a system. This results in analysis and reporting of events as it happens.

Batch jobs can be weekly, daily, hourly and also higher frequency.
Technologies: Python scripts, SQL, Spark, Flink.
    Python scripts can be run in Kubernetes, AWS batch... 
    To orchestrate all these batch jobs we will use airflow. 

* :movie_camera: 5.1.2 Introduction to Spark

[![](https://markdown-videos-api.jorgenkh.no/youtube/FhaqbEOuQ8U)](https://youtu.be/FhaqbEOuQ8U&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=52)

Apache Spark is a analytics engine for large scale data processing.
Sparks pulls the data to their executers and then outputs to another db for example. Is an engine because the processing happens in spark. It can also be in a cluster.
It is multi language for java and scale. For python there is a wrapper, called PySpark.
It can be used for both batch and streaming processing.
It is tipically used when data is in a data lake, like S3 of GCS. Then sparks makes processing nd put again in Data lake. Normally you can used bigquery or SQL in the DL, but if you can not really use SQL for the processing, you can use Spark.
in a nutshell:
Raw Data -> LAKE -> SQL -> SPARK -> PYTHON Train ML  


## 5.2 Installation

Follow [these instructions](setup/) to install Spark:

* [Windows](setup/windows.md)
* [Linux](setup/linux.md)
* [MacOS](setup/macos.md)

And follow [this](setup/pyspark.md) to run PySpark in Jupyter

* :movie_camera: 5.2.1 (Optional) Installing Spark (Linux)

[![](https://markdown-videos-api.jorgenkh.no/youtube/hqUbB9c8sKg)](https://youtu.be/hqUbB9c8sKg&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=53)

Alternatively, if the setups above don't work, you can run Spark in Google Colab.
> [!NOTE]  
> It's advisable to invest some time in setting things up locally rather than immediately jumping into this solution

* [Google Colab Instructions](https://medium.com/gitconnected/launch-spark-on-google-colab-and-connect-to-sparkui-342cad19b304)
* [Google Colab Starter Notebook](https://github.com/aaalexlit/medium_articles/blob/main/Spark_in_Colab.ipynb)

 

run spark-shell

val data = 1 to 10000
val distData = sc.parallelize(data)
distData.filter(_ < 10).collect()


add top bashrc:

PYTHONPATH="/usr/bin/python3.12"; export PYTHONPATH;
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip":$PYTHONPATH



## 5.3 Spark SQL and DataFrames

* :movie_camera: 5.3.1 First Look at Spark/PySpark

[![](https://markdown-videos-api.jorgenkh.no/youtube/r_Sf6fCB40c)](https://youtu.be/r_Sf6fCB40c&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=54)

- Reading CSV files
- Partitions
- Saving data to Parquet for local experiments
- Spark master UI

in localhost:4040 we have the pyspark master application UI


* :movie_camera: 5.3.2 Spark Dataframes

[![](https://markdown-videos-api.jorgenkh.no/youtube/ti3aC1m3rE8)](https://youtu.be/ti3aC1m3rE8&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=55)

- Actions vs transformations
- Functions and UDFs


* :movie_camera: 5.3.3 (Optional) Preparing Yellow and Green Taxi Data

[![](https://markdown-videos-api.jorgenkh.no/youtube/CI3P4tAtru4)](https://youtu.be/CI3P4tAtru4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=56)

Script to prepare the Dataset [download_data.sh](code/download_data.sh)

> [!NOTE]  
> The other way to infer the schema (apart from pandas) for the csv files, is to set the `inferSchema` option to `true` while reading the files in Spark.

* :movie_camera: 5.3.4 SQL with Spark

[![](https://markdown-videos-api.jorgenkh.no/youtube/uAlp2VuZZPY)](https://youtu.be/uAlp2VuZZPY&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=57)


## 5.4 Spark Internals

* :movie_camera: 5.4.1 Anatomy of a Spark Cluster

[![](https://markdown-videos-api.jorgenkh.no/youtube/68CipcZt7ZA)](https://youtu.be/68CipcZt7ZA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=58)

* :movie_camera: 5.4.2 GroupBy in Spark

[![](https://markdown-videos-api.jorgenkh.no/youtube/9qrDsY_2COo)](https://youtu.be/9qrDsY_2COo&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=59)

* :movie_camera: 5.4.3 Joins in Spark

[![](https://markdown-videos-api.jorgenkh.no/youtube/lu7TrqAWuH4)](https://youtu.be/lu7TrqAWuH4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=60)

## 5.5 (Optional) Resilient Distributed Datasets

* :movie_camera: 5.5.1 Operations on Spark RDDs

[![](https://markdown-videos-api.jorgenkh.no/youtube/Bdu-xIrF3OM)](https://youtu.be/Bdu-xIrF3OM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=61)

* :movie_camera: 5.5.2 Spark RDD mapPartition

[![](https://markdown-videos-api.jorgenkh.no/youtube/k3uB2K99roI)](https://youtu.be/k3uB2K99roI&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=62)


## 5.6 Running Spark in the Cloud

* :movie_camera: 5.6.1 Connecting to Google Cloud Storage

[![](https://markdown-videos-api.jorgenkh.no/youtube/Yyz293hBVcQ)](https://youtu.be/Yyz293hBVcQ&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=63)

* :movie_camera: 5.6.2 Creating a Local Spark Cluster

[![](https://markdown-videos-api.jorgenkh.no/youtube/HXBwSlXo5IA)](https://youtu.be/HXBwSlXo5IA&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=64)

* :movie_camera: 5.6.3 Setting up a Dataproc Cluster

[![](https://markdown-videos-api.jorgenkh.no/youtube/osAiAYahvh8)](https://youtu.be/osAiAYahvh8&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=65)

* :movie_camera: 5.6.4 Connecting Spark to Big Query

[![](https://markdown-videos-api.jorgenkh.no/youtube/HIm2BOj8C0Q)](https://youtu.be/HIm2BOj8C0Q&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=66)


# Homework

* [2025 Homework](../cohorts/2025/05-batch/homework.md)


# Community notes

Did you take notes? You can share them here.

* [Notes by Alvaro Navas](https://github.com/ziritrion/dataeng-zoomcamp/blob/main/notes/5_batch_processing.md)
* [Sandy's DE Learning Blog](https://learningdataengineering540969211.wordpress.com/2022/02/24/week-5-de-zoomcamp-5-2-1-installing-spark-on-linux/)
* [Notes by Alain Boisvert](https://github.com/boisalai/de-zoomcamp-2023/blob/main/week5.md)
* [Alternative : Using docker-compose to launch spark by rafik](https://gist.github.com/rafik-rahoui/f98df941c4ccced9c46e9ccbdef63a03) 
* [Marcos Torregrosa's blog (spanish)](https://www.n4gash.com/2023/data-engineering-zoomcamp-semana-5-batch-spark)
* [Notes by Victor Padilha](https://github.com/padilha/de-zoomcamp/tree/master/week5)
* [Notes by Oscar Garcia](https://github.com/ozkary/Data-Engineering-Bootcamp/tree/main/Step5-Batch-Processing)
* [Notes by HongWei](https://github.com/hwchua0209/data-engineering-zoomcamp-submission/blob/main/05-batch-processing/README.md)
* [2024 videos transcript](https://drive.google.com/drive/folders/1XMmP4H5AMm1qCfMFxc_hqaPGw31KIVcb?usp=drive_link) by Maria Fisher 
* [2025 Notes by Manuel Guerra](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes/blob/main/5_Batch-Processing-Spark/README.md)
* [2025 Notes by Gabi Fonseca](https://github.com/fonsecagabriella/data_engineering/blob/main/05_batch_processing/00_notes.md)
* [2025 Notes on Installing Spark on MacOS (with Anaconda + brew) by Gabi Fonseca](https://github.com/fonsecagabriella/data_engineering/blob/main/05_batch_processing/01_env_setup.md)
* Add your notes here (above this line)
