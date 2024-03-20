#TB! load env ariables
import our_utilities; our_utilities.load_env_with_substitutions()

from dagster import asset, AssetIn, AssetKey, AssetMaterialization, AssetExecutionContext, DagsterInstance, MetadataValue

import pandas as pd
from typing import Dict

from ...resources.resources import MyAWSS3Resource

@asset
def get_new_s3_files(context: AssetExecutionContext,
                     s3_with_bucket: MyAWSS3Resource):
    s3_client = s3_with_bucket.create_s3_client()
    bucket = s3_with_bucket.bucket_name

    dagster_instance = DagsterInstance.get()

    paginator = s3_client.get_paginator('list_objects')
    new_files = []
    for result in paginator.paginate(Bucket=bucket):
        for file in result.get('Contents', []):
            file_name = file['Key']
            context.log.info(f"Scanning {file_name} file...")
            if not dagster_instance.has_asset_key(AssetKey(file_name)):
                new_files.append({'bucket': bucket, 'key': file_name})

    return new_files


@asset(ins={"new_files": AssetIn(key=AssetKey("get_new_s3_files"))})
def the_s3_files_as_dict_of_dataframes(context: AssetExecutionContext, 
                                s3_with_bucket: MyAWSS3Resource,
                                new_files: list) -> Dict:
    s3_client = s3_with_bucket.create_s3_client()
    result = {}  # dictionary to collect data frames

    for s3_coordinate in new_files:
        bucket = s3_coordinate['bucket']
        key = s3_coordinate['key']
        data = s3_client.get_object(Bucket=bucket, Key=key)

        # first test if the data is a csv file
        if data['ContentType'] != 'text/csv':
            # continue to the next file
            continue
        
        df = pd.read_csv(data['Body'])
        result[key] = df  # add data frame to the dictionary

    context.add_output_metadata(
        metadata={
            "num_of_files": len(result),
            # The `MetadataValue` class has useful static methods to build Metadata
        }
    )

    context.log.info("Created the assets Dataframe dict from the S3 files.")

    # Yield the dictionary of data frames
    return result



@asset(ins={"new_files": AssetIn(key=AssetKey("get_new_s3_files"))})
def materialize_the_assets_in_dagster(context: AssetExecutionContext, 
                                s3_with_bucket: MyAWSS3Resource,
                                new_files: list) -> Dict:
    s3_client = s3_with_bucket.create_s3_client()

    for s3_coordinate in new_files:
        bucket = s3_coordinate['bucket']
        key = s3_coordinate['key']
        data = s3_client.get_object(Bucket=bucket, Key=key)

        # first test if the data is a csv file
        if data['ContentType'] != 'text/csv':
            # continue to the next file
            continue
        
        df = pd.read_csv(data['Body'])

        # Yield an AssetMaterialization for each DataFrame
        yield AssetMaterialization(
            asset_key=key,
            description="Created asset from S3 file",
            metadata={
                "num_records": len(df),
                "preview": MetadataValue.md(df.head().to_markdown()),
                "shape": str(df.shape),
                "dtypes": df.dtypes.to_string(),
            },
        )

        context.log.info("Materialized the assets in Dagster GUI.")

