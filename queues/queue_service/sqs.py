import json

import boto3
import botocore

from config import REGION_AWS
from queues.queue_manager import QueueFacade


class SimpleQueueAmazon(QueueFacade):

    def __init__(self):
        self.connected = True
        self.client = boto3.client('sqs', region_name=REGION_AWS)
        self.try_connect()

    @staticmethod
    def get_url_queue(name: str):
        return f'https://sqs.{REGION_AWS}.amazonaws.com/321479814345/{name}'

    def try_connect(self):
        if self.connected is False:
            try:
                self.client = boto3.client('sqs', region_name=REGION_AWS)
            except botocore.exceptions.ClientError:
                self.connected = False

    def send_messages(self, items: list, name: str, batch_size: int = 10):
        items_to_send = []
        for item in items:
            items_to_send.append(
                {
                    "Id": str(len(items_to_send) + 1),
                    "MessageBody": json.dumps(item)
                }
            )

            if len(items_to_send) >= batch_size:
                self.send_batch_to_sqs(items_to_send, name)
                items_to_send = []

        if len(items_to_send) > 0:
            self.send_batch_to_sqs(items_to_send, name)

    def send_batch_to_sqs(self, items: list, name: str):
        self.try_connect()
        if self.connected is False:
            return None

        response = self.client.send_message_batch(
            QueueUrl=self.get_url_queue(name),
            Entries=items
        )
        return response

    def pull_messages(self, name: str, batch_size) -> list:
        self.try_connect()
        if self.connected is False:
            return []
        items = []
        while len(items) < batch_size:
            response = self.client.receive_message(
                QueueUrl=self.get_url_queue(name),
                AttributeNames=[
                    'SentTimestamp'
                ],
                MaxNumberOfMessages=10,
                MessageAttributeNames=[
                    'All'
                ],
                VisibilityTimeout=600,
                WaitTimeSeconds=0
            )
            if 'Messages' in response:
                for message in response['Messages']:
                    rh = message["ReceiptHandle"]
                    body = message["Body"]
                    body = json.loads(body)
                    if "item" in body:
                        item = body['item']
                    else:
                        item = body
                    item['ReceiptHandler'] = rh
                    items.append(item)

            else:
                break
        return items

    def delete_messages_queue(self, name: str, items: list):
        responses_delete_items = list()
        for item in items:
            response = self.client.delete_message(
                QueueUrl=self.get_url_queue(name),
                ReceiptHandle=item['ReceiptHandler']
            )
            responses_delete_items.append(response)
        return responses_delete_items

    def get_number_items(self, name: str) -> int:
        x = self.client.get_queue_attributes(QueueUrl=self.get_url_queue(name), AttributeNames=[
            'ApproximateNumberOfMessages',
            'ApproximateNumberOfMessagesDelayed',
        ])
        return int(x['Attributes']['ApproximateNumberOfMessages']) + int(x['Attributes'][
                                                                             'ApproximateNumberOfMessagesDelayed'])
