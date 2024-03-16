#################################################################
# Project Name: Transfer Salesforce Marketing Cloud into Snowflake 
# Author: Ryan Zhang 
# Changelog: 
# - Created on 18/Feb/2024
#
#
#################################################################


from datetime import timedelta, datetime, date
import json 
import os
import requests 
import pysftp
import pandas as pd 
import fnmatch

from airflow import DAG 
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

## local remote file paths...
gRemoteFP = '/Export/SFMCExport/TEST/'
gLocalFP = '/home/ubuntu/datasets/'
gLocalTargetFolder = '/home/ubuntu/response_data/'
sftpHostname = '########'
sftpUsername = '########'
sftpPassword = '########'

# Define the task_id and the source file path using the dynamically generated filename
filename = f"dv_sent_{datetime.now().strftime('%Y%m%d')}.csv"
source_file_path = f"/home/ubuntu/response_data/{filename}"

# Download Files from SFTP
def downloadFlles():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    try:
        files = os.listdir(gLocalFP)

        files_list = [file for file in files if fnmatch.fnmatch(file, 'dv_sent*.csv')]

        files_list = sorted(files_list, reverse=True)

        # check if sys output todays` data
        today = date.today().strftime("%Y%m%d")
        file_latest_check = 'dv_sent' + '_' + today
        output_file_path = f"/home/ubuntu/response_data_{today}.csv"

        if file_latest_check != files_list[0]:
            files_latest = files_list[0]
            # print(files_latest)
            # print(gLocalFP + files_latest)

            df = pd.read_csv(os.path.join(gLocalFP, files_latest))
            output_file_path = os.path.join(gLocalTargetFolder, f'dv_sent_{today}.csv')
            return df.to_csv(output_file_path, index=False)
        # if sys doesn`t output today`s data then return None
        else: 
            return None
    
    except Exception as e:
        if hasattr(e, 'message'):
            print('Execption occured in downloadFiles() ' + e.message)
        else:
            print ('Execption occured in downloadFiles() ' + e)



# Make Default DAGs...
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 3, 1),
    'email': 'this_is_my_fake_email@email.com',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}

with DAG('sfmc_transfer_dag',
         default_args = default_args,
         schedule_interval = '@daily',
         catchup=False
         ) as dag:
    
    extact_sfmc_dv_sent_data_var = PythonOperator(
        task_id = 'tsk_extract_dv_sent_from_stfp',
        python_callable = downloadFlles
    )

    # Define the BashOperator
    load_to_s3 = BashOperator(
        task_id='tsk_load_to_s3',
        bash_command=f'aws s3 mv {source_file_path} s3://dataview-sfmcdata/'
    )
    
    # check if files is already in s3 bucket
    is_file_in_s3_landingzone = S3KeySensor(
        task_id = 'is_file_in_s3',
        bucket_key = f'dv_sent_{datetime.now().strftime("%Y%m%d")}.csv',
        bucket_name = 'dataview-sfmcdata',
        aws_conn_id = 'aws_s3_conn',
        wildcard_match=False,  # Set this to True if you want to use wildcards in the prefix
        timeout = 120,
        poke_interval = 5,
    ) 

    extact_sfmc_dv_sent_data_var >> load_to_s3 >> is_file_in_s3_landingzone 
