# SFMC-Data-Pipelines

## Overview
![image](https://github.com/Ryan-FanZhang/SFMC-Data-Pipelines/blob/e37df51a8b7b7b7eb5cef2f5a0776c83a6cdbbfd/Airflow-pieplines.png)
This project automates the processing of daily salesforce marketing data from SFTP using AWS services, Airflow and Snowflake. CSV files containing email records are uploaded to an S3 bucket (Landing Zone), triggering an AWS Lambda function to copy raw data and load into an S3 bucket (Intermediate Zone), triggering an AWS lambda function to transform and load into an S3 bucket (Transformed Zone). Notifications are sent via Amazon SNS. 
Finally, Snowflake will automate grabbing data and loading it into the target schema.

## Requirements
<ol>
- AWS Account
- Amazon S3 buckets: landing zone, intermediate zone and transformed zone
- AWS Lambda
- Amazon SNS
- AWS IAM (for permissions)
- GitHub (for version control)
- Python, pandas library, Snowpark, SQL Alchemy
- Email subscription for SNS notifications
<ol>

## Steps

