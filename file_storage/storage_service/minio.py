import boto3

from botocore.config import Config

from file_storage.storage_service.s3 import S3


class Minio(S3):
    def __init__(self, region_name: str, endpoint_minio: str):
        """
        :param region_name: Name of the region to connect with the API
        """
        super().__init__(region_name)
        self.s3 = boto3.client('s3', endpoint_url=endpoint_minio,
                               config=Config(signature_version='s3v4'),
                               region_name=region_name)
        self.paginator = self.s3.get_paginator("list_objects_v2")
