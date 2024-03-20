#TB! load env ariables
import our_utilities; our_utilities.load_env_with_substitutions()

from dagster import ConfigurableResource

import boto3
from botocore import UNSIGNED
from botocore.client import Config

class MyAWSS3Resource(ConfigurableResource):
    bucket_name: str

    def create_s3_client(self):

        s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

        return s3
