import json
import pandas as pd 
import boto3
from datetime import datetime, date
from io import StringIO

filename = f"dv_sent_{datetime.now().strftime('%Y%m%d')}.csv"
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # TODO implement
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    print("source_bucket:", source_bucket)
    print("object_key:", object_key)
    
    target_bucket = 'dataview-sfmcdata-cleaned'
    target_files = filename
    print("target_files:", filename)
    
    response = s3_client.get_object(Bucket=source_bucket, Key=object_key)
    csv_content = response['Body'].read().decode('utf-8')
    
    # Read CSV content into DataFrame
    dataframe = pd.read_csv(StringIO(csv_content))
    print(dataframe.head(5))
    csv_data = dataframe.to_csv(index = False)
    
    # Upload CSV to S3
    s3_client.put_object(Bucket=target_bucket, Key=filename, Body=csv_data)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Move files successfully')
    }
