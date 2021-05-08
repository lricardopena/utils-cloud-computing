from copy import deepcopy

from queues.queue_manager import QueueFacade


class QueueSingleton(type, QueueFacade):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Local(metaclass=QueueSingleton):
    queue: dict

    def __init__(self):
        self.queue = {}

    def send_messages(self, items: list, name: str, batch_size: int = 10):
        if name not in self.queue:
            self.queue[name] = []
        self.queue[name].extend([item for item in deepcopy(items)])

    def pull_messages(self, name: str, n_items: int) -> list:
        result = list()
        if name not in self.queue:
            return []

        for i in range(0, n_items):
            if len(self.queue[name]) == 0:
                break
            result.append(self.queue[name].pop())
        return result

    def delete_messages_queue(self, name: str, items: list) -> list:
        pass

    def get_number_items(self, name: str) -> int:
        return len(self.queue[name])
