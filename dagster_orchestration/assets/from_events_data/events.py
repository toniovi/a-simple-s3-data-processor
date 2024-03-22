#TB! load env ariables
import our_utilities; our_utilities.load_env_with_substitutions()

from dagster import (asset, AssetIn, AssetKey, AssetMaterialization, 
                     AssetExecutionContext, DagsterInstance, MetadataValue, 
                     DynamicOut, DynamicOutput, DynamicPartitionsDefinition)

import pandas as pd
from typing import Dict

from ...resources.resources import MyAWSS3Resource

files_partitions_def = DynamicPartitionsDefinition(name="new_s3_files")

@asset(partitions_def=files_partitions_def)
def get_new_s3_files(context: AssetExecutionContext,
                     s3_with_bucket: MyAWSS3Resource):
    s3_client = s3_with_bucket.create_s3_client()
    bucket = s3_with_bucket.bucket_name

    new_files = []
    paginator = s3_client.get_paginator('list_objects')

    for result in paginator.paginate(Bucket=bucket):
        for file in result.get('Contents', []):
            file_name = file['Key']
            context.log.info(f"Scanning {file_name} file...")
            # We assign generation to dynamic partitions instead of asset keys
            if not context.has_dynamic_partition(files_partitions_def.name, file_name):
                new_files.append({'bucket': bucket, 'key': file_name})


    # Generate dynamic partitions from new files
    context.dynamic_partitioned_output.add_dynamic_partitions([(new_file['key'], {}) for new_file in new_files])
    
    return new_files


@asset(partitions_def=files_partitions_def,
       ins={"new_files": AssetIn(key=AssetKey("get_new_s3_files"))})
def the_s3_files_as_dict_of_dataframes(context: AssetExecutionContext, 
                                s3_with_bucket: MyAWSS3Resource,
                                new_files: list) -> None:
    s3_client = s3_with_bucket.create_s3_client()
    dataframes = {}

    for s3_coordinate in new_files:
        bucket = s3_coordinate['bucket']
        key = s3_coordinate['key']
        data = s3_client.get_object(Bucket=bucket, Key=key)

        # first test if the data is a csv file
        if data['ContentType'] != 'text/csv':
            df = pd.read_csv(data['Body'])
            dataframes[key] = df  # add data frame to the dictionary

            # We can yield each df as a dynamic partitioned output if needed
            yield DynamicOutput(
                value=df,
                mapping_key=key.replace('/', '_').replace('.', '_'),  # sanitize the key for use as a mapping key
                output_name="dataframes"
            )

            context.log.info(f"Created dataframe asset for the S3 file: {key}")
        
        #return dataframes

   


# @asset(ins={"new_files": AssetIn(key=AssetKey("get_new_s3_files"))})
# def materialize_the_assets_in_dagster(context: AssetExecutionContext, 
#                                 s3_with_bucket: MyAWSS3Resource,
#                                 new_files: list) -> Dict:
#     s3_client = s3_with_bucket.create_s3_client()

#     for s3_coordinate in new_files:
#         bucket = s3_coordinate['bucket']
#         key = s3_coordinate['key']
#         data = s3_client.get_object(Bucket=bucket, Key=key)

#         # first test if the data is a csv file
#         if data['ContentType'] != 'text/csv':
#             # continue to the next file
#             continue
        
#         df = pd.read_csv(data['Body'])

#         # Yield an AssetMaterialization for each DataFrame
#         yield AssetMaterialization(
#             asset_key=key,
#             description="Created asset from S3 file",
#             metadata={
#                 "num_records": len(df),
#                 "preview": MetadataValue.md(df.head().to_markdown()),
#                 "shape": str(df.shape),
#                 "dtypes": df.dtypes.to_string(),
#             },
#         )

#         context.log.info("Materialized the assets in Dagster GUI.")

