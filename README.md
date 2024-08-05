# Real-time Data Pipeline with Kafka, Spark, S3, AWS Glue, Athena, and Redshift

This project uses a real-time data streaming pipeline to monitor a smart road and analyze data coming it. The pipeline leverages a combination of tools and services including: Python, Docker, Apache Zookeeper, Apache Kafka, Apache Spark, AWS S3, AWS Cloud, AWS Glue, AWS Athena, AWS Redshift.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [System Setup](#system-setup)

## Overview

The pipeline is designed to:

1. Kafka receive real-time data from 5 IoT-like data generators and forward data to Spark Cluster.
2. Spark Streaming receive the data transform it and load it in a Data Lake (AWS S3)
3. Transform the data in S3 using AWS Glue and Amazon Athena.
4. Load the transformed data into Amazon Redshift for analytics and querying.

## Architecture
![RedditDataEngineering.png](assets%2FRedditDataEngineering.png)
1. **Data Generators**: Five data generators that simulate IOT devices in a smart road.
2. **Apache Kafka**: Message Broker receive data from the five data generator and deliver it to Spark.
3. **Apache Spark**: Process real-time data within its cluster consisting of a master node and 2 worker nodes.
4. **Amazon S3**: Raw data storage.
5. **AWS Glue**: Data cataloging and ETL jobs.
6. **Amazon Athena**: SQL-based data transformation.
7. **Amazon Redshift**: Data warehousing and analytics.

## Prerequisites
- AWS Account with appropriate permissions for S3, Glue, Athena, and Redshift.
- Docker Installation
- Python 3.9

## System Setup
1. Clone the repository.
   ```bash
    git clone https://github.com/AmrAlashram/Smart-Road-Monitoring-and-Analysis-System.git
   ```
2. Create a virtual environment.
   ```bash
    python3 -m venv venv
   ```
3. Activate the virtual environment.
   ```bash
    source venv/bin/activate
   ```
4. Install the dependencies.
   ```bash
    pip install -r requirements.txt
   ```
5. Rename the configuration file and the credentials to the file.
   ```bash
    mv jobs/config.conf.example jobs/config.conf
   ```
6. Launch the system by starting the containers
   ```bash
    docker-compose up -d
   ```


