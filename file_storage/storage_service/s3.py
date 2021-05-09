import logging
import os
from datetime import datetime
from io import BytesIO

import boto3
from botocore.exceptions import ClientError

from file_storage.file_storage_manager import FileStorageManager


class S3(FileStorageManager):
    def __init__(self, bucket: str, region_name: str):
        """
        :param region_name: The region to connect to AWS
        """
        self.client = boto3.client('s3', region_name=region_name)
        self.paginator = self.client.get_paginator("list_objects_v2")
        self.bucket = bucket
        super().__init__()

    def put_file(self, file_name: str, value: BytesIO):
        """
        This function put some object in the bucket named (key) as send by the file_name
        :param file_name: Name to save in the bucket
        :param value: The buffer to save in the
        :return: None
        """
        value.seek(0)
        self.client.upload_fileobj(value, self.bucket, file_name)

    def get_file(self, file_name: str) -> BytesIO:
        """
        Function that gets the file from the file_name
        :param file_name:
        :return:
        """
        fl = BytesIO()
        self.client.download_fileobj(self.bucket,  file_name, fl)
        fl.seek(0)
        return fl

    def get_last_update(self, file_name: str) -> datetime:
        pages = self.paginator.paginate(
            Bucket=self.bucket,
            Prefix=file_name
        )

        for page in pages:
            for paged_file in page['Contents']:
                return paged_file['LastModified']
        # If the file isn't there we return an long date
        return datetime(1, 1, 1, 0, 0)

    def get_filenames_prefix(self, prefix):
        pages = self.paginator.paginate(
            Bucket=self.bucket,
            Prefix=self.base_path + prefix
        )
        file_names = []

        for page in pages:
            for paged_file in page['Contents']:
                file_names.append(paged_file['Key'])
                print(paged_file['Key'])

        return [filename[len(self.base_path):] for filename in file_names]

    def file_exists(self, file_name: str) -> bool:
        pages = self.paginator.paginate(
            Bucket=self.bucket,
            Prefix=os.path.join(self.base_path, file_name)
        )

        for page in pages:
            for paged_file in page['Contents']:
                return True
        # If the file isn't there
        return False

    def move_filenames_to_prefix(self, file_names: list, prefix: str):
        for file_name in file_names:
            copy_source = {
                'Bucket': self.bucket,
                'Key': os.path.join(self.base_path, file_name)
            }

            self.client.copy(copy_source, self.bucket, os.path.join(prefix, file_name))
            self.delete(file_name)

    def delete(self, file_name: str):
        self.client.delete_object(Bucket=self.bucket, Key=os.path.join(self.base_path, file_name))

    def create_bucket(self, bucket_name: str):
        """Create an S3 bucket in a specified region

        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).

        :param bucket_name: Bucket to create
        :return: True if bucket created, else False
        """

        # Create bucket
        try:
            self.client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True
