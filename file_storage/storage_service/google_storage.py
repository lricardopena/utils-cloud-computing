import os
from datetime import datetime
from io import BytesIO

import boto3

from google.cloud import storage

from file_storage.file_storage_manager import FileStorageManager
from file_storage.storage_service.s3 import S3

DELIMITER = '/'


class GoogleStorage(FileStorageManager):
    def __init__(self, bucket: str):
        """
        :param bucket: Bucket name
        """
        super().__init__()
        self.client = storage.Client()
        self.bucket_object = self.client.bucket(bucket)

    def put_file(self, file_name: str, value: BytesIO):
        self.bucket_object.upload_from_file(value)

    def get_file(self, file_name: str) -> BytesIO:
        value = BytesIO()
        self.bucket_object.download_blob_to_file(file_name, value)
        return value

    def delete(self, file_name: str):
        blob = self.bucket_object.blob(file_name)
        blob.delete()

    def get_last_update(self, file_name: str) -> datetime:
        blob = self.bucket_object.get_blob(file_name)
        return blob.updated

    def file_exists(self, file_name: str) -> bool:
        return storage.Blob(bucket=self.bucket_object, name=file_name).exists(self.client)

    def get_filenames_prefix(self, prefix: str):
        blobs = self.client.list_blobs(self.bucket_object, prefix=prefix, delimiter=DELIMITER)

        file_names = []
        for blob in blobs:
            file_names.append(blob.name)

        return file_names

    def move_filenames_to_prefix(self, file_names: list, prefix: str):
        for file_name in file_names:
            source_blob = self.bucket_object.blob(file_name)

            self.bucket_object.copy_blob(
                source_blob, self.bucket_object, os.path.join(prefix, file_name)
            )

    def create_bucket(self, bucket_name: str, location: str = None):
        bucket = self.client.bucket(bucket_name)
        bucket.storage_class = "COLDLINE"
        new_bucket = self.client.create_bucket(bucket, location=location)
        return new_bucket


class GoogleStorageFromS3(S3):
    def __init__(self, bucket: str, base_path: str, region_name: str):
        """
        :param bucket:
        :param base_path:
        :param region_name:
        """
        super().__init__(bucket, base_path)
        self.client = boto3.client("s3", region_name=region_name, endpoint_url="https://storage.googleapis.com")
        self.paginator = self.client.get_paginator("list_objects_v2")
