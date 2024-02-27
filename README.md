# Data Extraction and Cleaning
Overview
## This project aims to create utility scripts for extracting and cleaning data from various sources. We’ll create three Python scripts: data_extraction.py, database_utils.py, and data_cleaning.py.

### 1. data_extraction.py
Create a class named DataExtractor.
This class will contain methods to extract data from different sources:
CSV files
An API
An S3 bucket
### 2. database_utils.py
Create a class named DatabaseConnector.
This class will handle database connections and data uploads.
### 3. data_cleaning.py
Create a class named DataCleaning.
Implement methods to clean data from each of the data sources.

## The data that we are fetching pertains to sales related inforamtion for a company where we have tables like: Product details, order details etc and we extract , clean this information before finally uploading it to our local database called sales data in Postgresql
