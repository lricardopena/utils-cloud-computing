from copy import deepcopy
from io import BytesIO

from file_storage.storage_service.localstack_s3 import LocalStackS3

NAME_BUCKET_EXAMPLE = 'example-bucket'
ENDPOINT_LOCALSTACK = 'http://localhost:4566/'
REGION_LOCALSTACK = 'us-east-1'

FILENAME_EXAMPLE = 'example_file'
EXAMPLE_FILE = BytesIO(b'Some example data')


if __name__ == '__main__':
    lstack = LocalStackS3(NAME_BUCKET_EXAMPLE, REGION_LOCALSTACK, ENDPOINT_LOCALSTACK)

    # Create the bucket if doesn't exist
    lstack.create_bucket(NAME_BUCKET_EXAMPLE)

    # Put an example of file-like type in the bucketCreate the bucket if doesn't exist
    lstack.put_file(FILENAME_EXAMPLE, deepcopy(EXAMPLE_FILE))

    # Ensure that the file exist
    file_exists = lstack.file_exists(FILENAME_EXAMPLE)
    assert file_exists, 'This point should never enter'

    file_read = lstack.get_file(FILENAME_EXAMPLE)

    bytes_read = file_read.read()

    assert bytes_read == EXAMPLE_FILE.read(), 'This assert will never appear, both bytes should be the same'

    print('End example with success')
