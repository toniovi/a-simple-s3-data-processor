#TB! load env ariables
import our_utilities; our_utilities.load_env_with_substitutions()

from dagster import sensor, RunRequest, SensorEvaluationContext, AssetKey
from dagster.core.instance import DagsterInstance

import os

from ..resources.resources import MyAWSS3Resource

@sensor()
def check_for_new_s3_files(context: SensorEvaluationContext,
                           s3_with_bucket: MyAWSS3Resource):
    s3_client = s3_with_bucket.create_s3_client()
    bucket = s3_with_bucket.bucket_name

    dagster_instance = DagsterInstance.get()

    paginator = s3_client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket):
        for file in result.get('Contents', []):
            file_name = file['Key']
            if not dagster_instance.has_asset_key(AssetKey(file_name)):
                yield RunRequest(run_key=None, run_config={})

# In this code:

# dagster_instance = instance.DagsterInstance.get() gets the current Dagster instance.
# if not dagster_instance.has_asset_key(asset_key): checks if the asset catalog of the Dagster instance already has an asset with the given key. If not, it yields a RunRequest for the process_s3_files_job job.
# This way, the sensor will only trigger the job for files that have not yet been processed into assets.
                    

