from queues.queue_service.sqs import SimpleQueueAmazon


class LocalStackSQS(SimpleQueueAmazon):
    def __init__(self, endpoint_localstack: str, region_name: str):
        super().__init__(endpoint_url=endpoint_localstack, region_name=region_name)
