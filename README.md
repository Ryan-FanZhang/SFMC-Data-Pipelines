# SFMC-Data-Pipelines

## Overview
![image](https://github.com/Ryan-FanZhang/SFMC-Data-Pipelines/blob/e37df51a8b7b7b7eb5cef2f5a0776c83a6cdbbfd/Airflow-pieplines.png)
This project automates the processing of daily salesforce marketing data from SFTP using AWS services, Airflow and Snowflake. CSV files containing email records are uploaded to an S3 bucket (Landing Zone), triggering an AWS Lambda function to copy raw data and load into an S3 bucket (Intermediate Zone), triggering an AWS lambda function to transform and load into an S3 bucket (Transformed Zone). Notifications are sent via Amazon SNS. 
Finally, Snowflake will automate grabbing data and loading it into the target schema.

## Requirements
<ol>
<li>AWS Account</li>
<li>Amazon S3 buckets: landing zone, intermediate zone and transformed zone</li>
<li>AWS Lambda</li>
<li>Amazon SNS</li>
<li>AWS IAM (for permissions)</li>
<li>GitHub (for version control)</li>
<li>Python, pandas library, Snowpark, SQL Alchemy</li>
<li>Email subscription for SNS notifications</li>
</ol>

## Steps

