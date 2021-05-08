import os
from datetime import datetime
from io import BytesIO

from file_storage.file_storage_manager import FileStorageManager


class Local(FileStorageManager):
    def __init__(self, base_path: str):
        self.base_path = base_path
        super().__init__()

    def final_path(self, file_name):
        finalpath = os.path.expanduser(os.path.join(self.base_path, file_name))
        return finalpath

    def put_file(self, file_name: str, value: BytesIO):
        value.seek(0)
        finalpath = self.final_path(file_name)
        fl = open(finalpath, "wb")
        with fl:
            fl.write(value.read())

    def get_file(self, file_name: str) -> BytesIO:
        value = BytesIO()
        finalpath = self.final_path(file_name)
        fl = open(finalpath, "rb")
        with fl:
            value.write(fl.read())
            value.seek(0)
            return value

    def delete(self, file_name: str):
        finalpath = self.final_path(file_name)
        if os.path.exists(finalpath):
            os.remove(finalpath)

    def get_last_update(self, file_name: str) -> datetime:
        finalpath = self.final_path(file_name)
        if not os.path.isfile(finalpath):
            return datetime(1, 1, 1, 0, 0)
        modified_time_unix = os.path.getmtime(finalpath)
        modification_time = datetime.fromtimestamp(modified_time_unix)
        return modification_time

    def get_filenames_prefix(self, prefix: str):
        name_files = [pos_json for pos_json in os.listdir(self.base_path + prefix)]
        name_files = [os.path.join(self.base_path, prefix, file_name) for file_name in name_files]
        return [filename[len(self.base_path):] for filename in name_files]
