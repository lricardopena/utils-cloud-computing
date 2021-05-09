from time import sleep

from queues.queue_service.localstack_sqs import LocalStackSQS

NAME_QUEUE_EXAMPLE = 'example-queue'
ENDPOINT_LOCALSTACK = 'http://localhost:4566/'
REGION_LOCALSTACK = 'us-east-1'
EXAMPLE_ITEM = {'message_body':
    {
        'example1': 'This is the first example to send',
        'example2': 'This is other example in the same item'
    }
}

if __name__ == '__main__':
    lstacksqs = LocalStackSQS(ENDPOINT_LOCALSTACK, region_name=REGION_LOCALSTACK)
    # First we create the queue
    lstacksqs.create_queue(NAME_QUEUE_EXAMPLE)

    lstacksqs.send_messages([EXAMPLE_ITEM], NAME_QUEUE_EXAMPLE)

    sleep(1)
    items_pulled = lstacksqs.pull_messages(NAME_QUEUE_EXAMPLE, 10)
    # For simplicity we add the key ReceiptHandler for a transparent use when we want to delete something.
    # Do what ever you want with the items (messages)

    # Don't forget to delete the message once you finish
    lstacksqs.delete_messages_queue(NAME_QUEUE_EXAMPLE, items_pulled)
