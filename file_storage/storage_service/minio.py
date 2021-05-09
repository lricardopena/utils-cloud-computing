from botocore.config import Config

from file_storage.storage_service.s3 import S3


class Minio(S3):
    def __init__(self, bucket: str, region_name: str, endpoint_minio: str):
        """
        :param bucket: Bucket Name to save the files in MinIO
        :param region_name: Name of the region to connect with the API
        :param endpoint_minio: The endpoint to connect with MinIO
        """
        super().__init__(bucket, region_name, endpoint_url=endpoint_minio, config=Config(signature_version='s3v4'))
