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
        page_iterator = paginator.paginate(Bucket=self.bucket_name, Delimiter='/')

        month_directories = []
        for page in page_iterator:
            for prefix_info in page.get('CommonPrefixes', []):
                prefix = prefix_info['Prefix']
                # Assuming the prefix format is "YYYY/MM/", we strip the "/" and replace with "_"
                stripped_prefix = prefix.strip('/').replace('/', '_')
                month_directories.append(stripped_prefix)

        return month_directories

