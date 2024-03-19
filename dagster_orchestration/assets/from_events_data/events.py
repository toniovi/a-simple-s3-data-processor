#TB! load env ariables
import our_utilities; our_utilities.load_env_with_substitutions()

import pandas as pd
from dagster import asset, AssetExecutionContext, job, AssetMaterialization
from dagster_aws.s3 import S3Coordinate
from dagster_aws.s3.resources import s3_resource


@asset
def create_asset_from_s3_file(context: AssetExecutionContext, s3_coordinate: S3Coordinate):
    s3_client = context.resources.s3
    bucket = s3_coordinate['bucket']
    key = s3_coordinate['key']
    data = s3_client.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(data['Body'])
    year, month, _ = key.split('/')
    nice_name = f"{year}_{month}_events"
    context.log.info(f"Created asset from {key} with nice name {nice_name}")
    yield AssetMaterialization(
        asset_key=nice_name,
        metadata={
            "num_records": len(df),
            "preview": df.head().to_markdown(),
            "path": key,
            "year": year,
            "month": month,
        }
    )
    yield df


@job(resource_defs={"s3": s3_resource})
def process_s3_files_job():
    create_asset_from_s3_file()


