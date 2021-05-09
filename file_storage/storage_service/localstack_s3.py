import boto3
from botocore.config import Config

from file_storage.storage_service.s3 import S3


class LocalStackS3(S3):
    def __init__(self, bucket: str, region_name: str, endpoint_localstack: str):
        """
        :param bucket: Bucket name
        :param region_name: Name of the region to connect with the API
        :param endpoint_localstack: Is the endpoint where the localstack is running, usually
        """
        self.bucket = bucket
        self.client = boto3.client('s3', endpoint_url=endpoint_localstack,
                                   config=Config(signature_version='s3v4'),
                                   region_name=region_name)
        self.paginator = self.client.get_paginator("list_objects_v2")
