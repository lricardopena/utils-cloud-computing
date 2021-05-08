from abc import ABC, abstractmethod
from datetime import datetime
from io import BytesIO


class FileStorageManager(ABC):
    base_path: str

    def __init__(self):
        pass

    @abstractmethod
    def put_file(self, file_name: str, value: BytesIO):
        pass

    @abstractmethod
    def get_file(self, file_name: str) -> BytesIO:
        pass

    @abstractmethod
    def delete(self, file_name: str):
        pass

    @abstractmethod
    def get_last_update(self, file_name: str) -> datetime:
        return datetime(1, 1, 1, 0, 0)

    @abstractmethod
    def file_exists(self, file_name: str) -> bool:
        pass

    @abstractmethod
    def get_filenames_prefix(self, prefix: str):
        pass

    @abstractmethod
    def move_filenames_to_prefix(self, file_names: list, prefix: str):
        pass
