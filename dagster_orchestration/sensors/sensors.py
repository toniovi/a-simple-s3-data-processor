#TB! load env ariables
import our_utilities; our_utilities.load_env_with_substitutions()

from dagster import sensor, RunRequest, instance
from ..assets.from_events_data.events import process_s3_files_job

@sensor(job=process_s3_files_job)
def check_for_new_s3_files(context):
    s3_client = context.resources.s3
    bucket = "work-sample-mk"
    dagster_instance = instance.DagsterInstance.get()
    paginator = s3_client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket):
        for file in result.get('Contents', []):
            file_name = file['Key']
            if file_name.endswith('events.csv'):
                year, month, _ = file_name.split('/')
                asset_key = f"{year}_{month}_events"
                if not dagster_instance.has_asset_key(asset_key):
                    yield RunRequest(run_key=file_name, run_config={
                        "ops": {
                            "create_asset_from_s3_file": {
                                "inputs": {
                                    "s3_coordinate": {
                                        "bucket": bucket,
                                        "key": file_name
                                    }
                                }
                            }
                        }
                    })


# In this code:

# dagster_instance = instance.DagsterInstance.get() gets the current Dagster instance.
# if not dagster_instance.has_asset_key(asset_key): checks if the asset catalog of the Dagster instance already has an asset with the given key. If not, it yields a RunRequest for the process_s3_files_job job.
# This way, the sensor will only trigger the job for files that have not yet been processed into assets.
                    

