-- truncate table SALESFORCEMARKETINGCLOUD.DATAVIEW.DV_SENT;

// create tables for dv_sent
create or replace TABLE SALESFORCEMARKETINGCLOUD.DATAVIEW.DV_SENT (
	DV_SENT_ID NUMBER(38,0),
	ACCOUNTID NUMBER(38,0),
	OYBACCOUNTID NUMBER(38,0),
	JOBID NUMBER(38,0),
	LISTID NUMBER(38,0),
	BATCHID NUMBER(38,0),
	SUBSCRIBERID NUMBER(38,0),
	SUBSCRIBERKEY VARCHAR(100),
	EVENTDATE TIMESTAMP_NTZ(9),
	DOMAIN VARCHAR(100),
	TRIGGERERSENDDEFINITIONOBJECTID VARCHAR(200),
	TRIGGEREDSENDCUSTOMERKEY VARCHAR(200),
	INSERT_DATE TIMESTAMP_NTZ(9),
	INSERT_FILENAME VARCHAR(200),
	LAST_MODIFIED_DATE VARCHAR(200),
	LAST_MODIFIED_FILENAME VARCHAR(200)
);

// check the table is already to be executed
select 
* from SALESFORCEMARKETINGCLOUD.DATAVIEW.DV_SENT limit 10;

select count(*) from SALESFORCEMARKETINGCLOUD.DATAVIEW.DV_SENT;

// define file format object 
create schema SALESFORCEMARKETINGCLOUD.file_format_schema;
create or replace file format salesforcemarketingcloud.file_format_schema.format_csv
    type = 'CSV'
    field_delimiter = ','
    RECORD_DELIMITER = '\n'
    skip_header = 1
    -- error_on_column_count_mismatch = FALSE;
;
// create staging csv
create schema SALESFORCEMARKETINGCLOUD.external_stage_schema;

// creating staging
create or replace stage salesforcemarketingcloud.external_stage_schema.sfmc_ext_stage_yml
    url = 's3://dataview-sfmcdata-cleaned/'
    credentials = (aws_key_id = 'This is my aws key id',
    aws_secret_key = 'This is my aws secret key') 
    file_format = salesforcemarketingcloud.file_format_schema.format_csv 
;

list @salesforcemarketingcloud.external_stage_schema.sfmc_ext_stage_yml;

// Create snowpipe schema
create or replace schema salesforcemarketingcloud.snowpipe_schema;

// create snowpipe 
create or replace pipe salesforcemarketingcloud.snowpipe_schema.sfmc_dv_sent_schema
auto_ingest = true
as 
copy into salesforcemarketingcloud.dataview.dv_sent
from @salesforcemarketingcloud.external_stage_schema.sfmc_ext_stage_yml;

desc pipe salesforcemarketingcloud.snowpipe_schema.sfmc_dv_sent_schema;


