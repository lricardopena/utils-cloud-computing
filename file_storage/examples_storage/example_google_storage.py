from copy import deepcopy
from io import BytesIO

from file_storage.storage_service.google_storage import GoogleStorage

NAME_BUCKET_EXAMPLE = 'example-bucket'
LOCATION_GOOGLE_CLOUD = 'us'

FILENAME_EXAMPLE = 'example_file'
EXAMPLE_FILE = BytesIO(b'Some example data')


if __name__ == '__main__':
    google_storage = GoogleStorage(NAME_BUCKET_EXAMPLE)

    # Create the bucket if doesn't exist
    google_storage.create_bucket(NAME_BUCKET_EXAMPLE, location=LOCATION_GOOGLE_CLOUD)

    # Put an example of file-like type in the bucketCreate the bucket if doesn't exist
    google_storage.put_file(FILENAME_EXAMPLE, deepcopy(EXAMPLE_FILE))

    # Ensure that the file exist
    file_exists = google_storage.file_exists(FILENAME_EXAMPLE)
    assert file_exists, 'This point should never enter'

    file_read = google_storage.get_file(FILENAME_EXAMPLE)

    bytes_read = file_read.read()

    assert bytes_read == EXAMPLE_FILE.read(), 'This assert will never appear, both bytes should be the same'

    print('End example with success')
