from time import sleep

from queues.queue_service.sqs import SimpleQueueAmazon

NAME_QUEUE_EXAMPLE = 'example-queue'
REGION_AWS = 'us-east-1'
EXAMPLE_ITEM = {'message_body':
    {
        'example1': 'This is the first example to send',
        'example2': 'This is other example in the same item'
    }
}

if __name__ == '__main__':
    queue_sqs = SimpleQueueAmazon(region_name=REGION_AWS)
    # If the doesn't exist you can uncomment the code below to create the queue
    # queue_sqs.create_queue(NAME_QUEUE_EXAMPLE)

    queue_sqs.send_messages([EXAMPLE_ITEM], NAME_QUEUE_EXAMPLE)

    sleep(1)
    items_pulled = queue_sqs.pull_messages(NAME_QUEUE_EXAMPLE, 10)
    # For simplicity we add the key ReceiptHandler for a transparent use when we want to delete something.

    # Do what ever you want with the items (messages)

    # Don't forget to delete the message once you finish
    queue_sqs.delete_messages_queue(NAME_QUEUE_EXAMPLE, items_pulled)
