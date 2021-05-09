from copy import deepcopy
from io import BytesIO

from file_storage.storage_service.localstorage import LocalStorage

BASE_PATH = '~/Trackstreet/file_manager_data/example'

FILENAME_EXAMPLE = 'example_file'
EXAMPLE_FILE = BytesIO(b'Some example data')


if __name__ == '__main__':
    local_storage = LocalStorage(BASE_PATH)

    # Put an example of file-like type in the bucketCreate the bucket if doesn't exist
    local_storage.put_file(FILENAME_EXAMPLE, deepcopy(EXAMPLE_FILE))

    # Ensure that the file exist
    file_exists = local_storage.file_exists(FILENAME_EXAMPLE)
    assert file_exists, 'This point should never enter'

    file_read = local_storage.get_file(FILENAME_EXAMPLE)

    bytes_read = file_read.read()

    assert bytes_read == EXAMPLE_FILE.read(), 'This assert will never appear, both bytes should be the same'

    print('End example with success')
