from botocore.config import Config

from file_storage.storage_service.s3 import S3


class LocalStackS3(S3):
    def __init__(self, bucket: str, region_name: str, endpoint_localstack: str):
        """
        :param bucket: Bucket name
        :param region_name: Name of the region to connect with the API
        :param endpoint_localstack: Is the endpoint where the localstack is running, usually
        """

        super().__init__(bucket, region_name, endpoint_url=endpoint_localstack,
                         config=Config(signature_version='s3v4'))
