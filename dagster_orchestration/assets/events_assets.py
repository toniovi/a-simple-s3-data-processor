#TB! load env variables
import our_utilities; our_utilities.load_env_with_substitutions()

from dagster import (asset, AssetExecutionContext, DynamicPartitionsDefinition, DynamicOutput)
import pandas as pd
from ..resources.s3_resources import MyAWSS3Resource

# Define the dynamic partitions definition
files_partitions_def = DynamicPartitionsDefinition(name="new_s3_files")

@asset(partitions_def=files_partitions_def)
def get_new_s3_files(context: AssetExecutionContext, s3_with_bucket: MyAWSS3Resource):
    s3_client = s3_with_bucket.create_s3_client()
    bucket = s3_with_bucket.bucket_name

    existing_partitions = context.instance.get_dynamic_partitions(files_partitions_def.name)
    
    # Define the function to calculate dynamic partitions based on existing files
    def list_new_monthly_files():
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket, Delimiter='/'):
            for prefix_info in page.get('CommonPrefixes', []):
                prefix = prefix_info['Prefix']
                # Assuming the prefix ends with "events.csv/", we strip and replace with "_"
                stripped_prefix = prefix.rstrip('events.csv/').replace('/', '_')
                if stripped_prefix not in existing_partitions:
                    yield stripped_prefix
    
    new_partitions = list(list_new_monthly_files())
    for partition in new_partitions:
        files_partitions_def.build_add_request([partition])
        #AttributeError: 'AssetExecutionContext' object has no attribute 'dynamic_partitioned_output'

    context.log.info(f"Created new_partitions")
    

    # Return the list of new partition keys found in the bucket, can be used for downstream processing
    return new_partitions


@asset(partitions_def=files_partitions_def)
def read_monthly_csv(context: AssetExecutionContext, s3_with_bucket: MyAWSS3Resource):
    
    partition_key = context.partition_key
    s3_client = s3_with_bucket.create_s3_client()
    bucket = s3_with_bucket.bucket_name
    key = f"{partition_key.replace('_', '/')}/events.csv"
    
    data = s3_client.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(data['Body'])
    context.log.info(f"Read dataframe from S3 file: {key}")

    return df

    # try:

        
    #     # yield DynamicOutput(
    #     #     value=df,
    #     #     mapping_key=partition_key,  # use the partition_key which is sanitized already
    #     # )
    # except Exception as error:
    #     context.log.error(f"Failed to read dataframe from S3 file: {key} due to: {error}")