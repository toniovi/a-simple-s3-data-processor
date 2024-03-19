from dagster import ScheduleDefinition
from .assets.from_events_data.events import process_s3_files_job

launch_sensor_every_five_minutes = ScheduleDefinition(job=process_s3_files_job, cron_schedule="*/5 * * * *")

