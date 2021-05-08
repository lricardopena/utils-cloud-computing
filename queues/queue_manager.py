class QueueFacade:

    def send_messages(self, items: list, name: str, batch_size: int = 10):
        pass

    def pull_messages(self, name: str, batch_size: int) -> list:
        pass

    def delete_messages_queue(self, name: str, items: list) -> list:
        pass

    def get_number_items(self, name: str) -> int:
        pass
