# SFMC-Data-Pipelines

## Overview
![image](https://github.com/Ryan-FanZhang/SFMC-Data-Pipelines/blob/e37df51a8b7b7b7eb5cef2f5a0776c83a6cdbbfd/Airflow-pieplines.png)
This project automates the processing of daily salesforce marketing data from SFTP using AWS services, Airflow and Snowflake. CSV files containing email records are uploaded to an S3 bucket (Landing Zone), triggering an AWS Lambda function to copy raw data and load into an S3 bucket (Intermediate Zone), triggering an AWS lambda function to transform and load into an S3 bucket (Transformed Zone). Notifications are sent via Amazon SNS. 
Finally, Snowflake will automate grabbing data and loading it into the target schema.

## Requirements
<ol>
<li>AWS Account</li>
<li>AAmazon S3 buckets: landing zone, intermediate zone and transformed zone</li>
<li>AAWS Lambda</li>
<li>AAmazon SNS</li>
<li>AAWS IAM (for permissions)</li>
<li>AGitHub (for version control)</li>
<li>APython, pandas library, Snowpark, SQL Alchemy</li>
<li>AEmail subscription for SNS notifications</li>
</ol>

## Steps

