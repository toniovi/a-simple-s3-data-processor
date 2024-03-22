#TB! load env variables
import our_utilities; our_utilities.load_env_with_substitutions()

from dagster import ConfigurableResource, make_values_resource

import boto3
from botocore import UNSIGNED
from botocore.client import Config

class MyAWSS3Resource(ConfigurableResource):
    bucket_name: str

    # def __init__(self, bucket_name: str):
    #     self.bucket_name = bucket_name

    def create_s3_client(self):
        # Here you can include additional configuration like region_name, access key, and secret key if needed
        s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
        return s3


    def list_month_directories(self):
        s3_client = self.create_s3_client()
        paginator = s3_client.get_paginator('list_objects_v2')

        month_directories = []
        # First, get the top-level directories (i.e., years)
        year_iterator = paginator.paginate(Bucket=self.bucket_name, Delimiter='/')
        for year_page in year_iterator:
            for year_info in year_page.get('CommonPrefixes', []):
                year_prefix = year_info['Prefix']
                # Then, for each year, get the subdirectories (i.e., months)
                month_iterator = paginator.paginate(Bucket=self.bucket_name, Prefix=year_prefix, Delimiter='/')
                for month_page in month_iterator:
                    for month_info in month_page.get('CommonPrefixes', []):
                        month_prefix = month_info['Prefix']
                        # Check if 'events.csv' exists in the directory
                        events_file = s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=f'{month_prefix}events.csv')
                        if 'Contents' in events_file:  # 'Contents' will be present if the file exists
                            # Format the prefix as "YYYY_MM"
                            formatted_prefix = month_prefix.strip('/').replace('/', '_')
                            month_directories.append(formatted_prefix)

        return month_directories