#TB! load env variables
import our_utilities; our_utilities.load_env_with_substitutions()

from dagster import sensor, SensorEvaluationContext, RunRequest

from ..assets.events_assets import files_partitions_def
from ..resources.s3_resources import MyAWSS3Resource


@sensor()
def check_for_new_s3_files(context: SensorEvaluationContext,
                           s3_with_bucket: MyAWSS3Resource):
    s3_with_bucket = s3_with_bucket.create_s3_client()
    existing_partitions = context.instance.all_partition_keys(files_partitions_def.name)

    # Retrieve the list of directories that represent months/year in the S3 bucket
    all_month_directories = s3_with_bucket.list_month_directories()

    new_partitions = [
        month for month in all_month_directories if month not in existing_partitions
    ]

    # Create run requests for new partitions not already tracked
    run_requests = [
        RunRequest(
            run_key=f'events_{month}',
            partition_key=month,
            tags={"month": month},
        )
        for month in new_partitions
    ]

    return run_requests