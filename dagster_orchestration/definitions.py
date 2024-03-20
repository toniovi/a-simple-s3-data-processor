#TB! load env ariables
import our_utilities; our_utilities.load_env_with_substitutions()

import os

from dagster import Definitions

from .assets.from_events_data.events import the_s3_files_as_dict_of_dataframes, get_new_s3_files, materialize_the_assets_in_dagster
from .sensors.sensors import check_for_new_s3_files
#from .schedules import launch_sensor_every_five_minutes
from .resources.resources import MyAWSS3Resource


defs = Definitions(
    assets=[the_s3_files_as_dict_of_dataframes, get_new_s3_files, materialize_the_assets_in_dagster],
    sensors=[check_for_new_s3_files],
    resources={
        "s3_with_bucket": MyAWSS3Resource(
            bucket_name=os.getenv("AWS_S3_BUCKET_NAME")
        ),
    },

)


