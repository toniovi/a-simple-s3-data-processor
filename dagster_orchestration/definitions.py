from dagster import Definitions
from .sensors.sensors import check_for_new_s3_files
from .assets.from_events_data.events import create_asset_from_s3_file, process_s3_files_job
from .schedules import launch_sensor_every_five_minutes

defs = Definitions(
    assets=[create_asset_from_s3_file],
    jobs=[process_s3_files_job],
    sensors=[check_for_new_s3_files],
    schedules = [
        launch_sensor_every_five_minutes,
    ],

)
