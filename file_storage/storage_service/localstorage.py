import os
from datetime import datetime
from io import BytesIO

from file_storage.file_storage_manager import FileStorageManager


class LocalStorage(FileStorageManager):
    def __init__(self, base_path: str):
        self.base_path = base_path
        super().__init__()

    def final_path(self, file_name):
        return os.path.expanduser(os.path.join(self.base_path, file_name))

    def put_file(self, file_name: str, value: BytesIO):
        value.seek(0)
        with open(self.final_path(file_name), "wb") as fl:
            fl.write(value.read())

    def get_file(self, file_name: str) -> BytesIO:
        value = BytesIO()
        with open(self.final_path(file_name), "rb") as fl:
            value.write(fl.read())
            value.seek(0)
            return value

    def delete(self, file_name: str):
        final_path = self.final_path(file_name)
        if os.path.exists(final_path):
            os.remove(final_path)

    def get_last_update(self, file_name: str) -> datetime:
        if not self.file_exists(file_name):
            return datetime(1, 1, 1, 0, 0)

        final_path = self.final_path(file_name)
        modified_time_unix = os.path.getmtime(final_path)
        modification_time = datetime.fromtimestamp(modified_time_unix)
        return modification_time

    def file_exists(self, file_name: str) -> bool:
        final_path = self.final_path(file_name)
        return os.path.isfile(final_path)

    def move_filenames_to_prefix(self, file_names: list, prefix: str):
        # Not implemented yet
        # TODO Implement this function
        pass

    def get_filenames_prefix(self, prefix: str):
        name_files = [pos_json for pos_json in os.listdir(self.base_path + prefix)]
        name_files = [os.path.join(self.base_path, prefix, file_name) for file_name in name_files]
        return [filename[len(self.base_path):] for filename in name_files]
