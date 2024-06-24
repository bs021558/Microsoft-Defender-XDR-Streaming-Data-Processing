import logging
import asyncio
from azure.eventhub.aio import EventHubConsumerClient

CONNECTION_STR = 'myconnectionstring'
CONSUMER_GROUP ='$Default'
EVENTHUB_NAME = 'myeventhubname'

logger = logging.getLogger("azure.eventhub")
logging.basicConfig(level=logging.INFO)

async def on_event(partition_context, event):
    logger.info("Received event from partition {}".format(partition_context.partition_id))
    logger.info(event.body_as_json()['records'][0])
    await asyncio.sleep(1)
    await partition_context.update_checkpoint(event)

async def receive():
    client = EventHubConsumerClient.from_connection_string(CONNECTION_STR, CONSUMER_GROUP, eventhub_name=EVENTHUB_NAME)
    async with client:
        await client.receive(
            on_event=on_event,
            starting_position="-1",  # "-1" is from the beginning of the partition.
        )
        # receive events from specified partition:
        # await client.receive(on_event=on_event, partition_id='0')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(receive())