#TB! load env ariables
import our_utilities; our_utilities.load_env_with_substitutions()

import os

from dagster import Definitions

from .assets.events_assets import get_new_s3_files, read_monthly_csv
from .sensors.events_sensors import check_for_new_s3_files
#from .schedules import launch_sensor_every_five_minutes
from .resources.s3_resources import MyAWSS3Resource


defs = Definitions(
    assets=[get_new_s3_files, read_monthly_csv],
    sensors=[check_for_new_s3_files],
    resources={
        "s3_with_bucket": MyAWSS3Resource(
            bucket_name=os.getenv("AWS_S3_BUCKET_NAME")
        ),
    },

)


