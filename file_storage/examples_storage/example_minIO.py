from copy import deepcopy
from io import BytesIO

from file_storage.storage_service.minio import Minio

NAME_BUCKET_EXAMPLE = 'example-bucket'
ENDPOINT_MINIO = 'http://172.17.0.2:9000/'
REGION_LOCALSTACK = 'us-east-1'

FILENAME_EXAMPLE = 'example_file'
EXAMPLE_FILE = BytesIO(b'Some example data')


if __name__ == '__main__':
    # Here we assume that you already have the MinIO configured like the aws credentials
    minio_storage = Minio(NAME_BUCKET_EXAMPLE, REGION_LOCALSTACK, ENDPOINT_MINIO)

    # Create the bucket if doesn't exist
    minio_storage.create_bucket(NAME_BUCKET_EXAMPLE)

    # Put an example of file-like type in the bucketCreate the bucket if doesn't exist
    minio_storage.put_file(FILENAME_EXAMPLE, deepcopy(EXAMPLE_FILE))

    # Ensure that the file exist
    file_exists = minio_storage.file_exists(FILENAME_EXAMPLE)
    assert file_exists, 'This point should never enter'

    file_read = minio_storage.get_file(FILENAME_EXAMPLE)

    bytes_read = file_read.read()

    assert bytes_read == EXAMPLE_FILE.read(), 'This assert will never appear, both bytes should be the same'

    print('End example with success')
