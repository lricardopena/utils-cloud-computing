from time import sleep

from queues.queue_service.localqueue import LocalQueue

NAME_QUEUE_EXAMPLE = 'example-queue'
EXAMPLE_ITEM = {'message_body':
    {
        'example1': 'This is the first example to send',
        'example2': 'This is other example in the same item'
    }
}

if __name__ == '__main__':
    queue_local = LocalQueue()

    queue_local.send_messages([EXAMPLE_ITEM], NAME_QUEUE_EXAMPLE)

    sleep(1)
    items_pulled = queue_local.pull_messages(NAME_QUEUE_EXAMPLE, 1)

    # Do what ever you want with the items (messages)

    queue_local.delete_messages_queue(NAME_QUEUE_EXAMPLE, items_pulled)
