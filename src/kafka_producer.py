import asyncio
from aiokafka import AIOKafkaProducer
from kafka import KafkaProducer
import json
from src.conf.urls import BROKER_URL

from src.logger import logger


producer: AIOKafkaProducer | None = None

producerJson: AIOKafkaProducer | None = None


STANDARD_DELAY = 5
MAX_DELAY = 30
delay = STANDARD_DELAY


async def start():
    global producer
    global producerJson
    global delay

    while True:
        try:
            producer = AIOKafkaProducer(bootstrap_servers=BROKER_URL)

            producerJson = AIOKafkaProducer(
                bootstrap_servers=BROKER_URL,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            await producer.start()
            await producerJson.start()
            return
        except Exception as e:
            logger.warning(f"can't connect to kafka. Failed by {e}")
            delay *= 1.4
            if delay >= MAX_DELAY:
                delay = MAX_DELAY
            await asyncio.sleep(delay)


def get_producer():
    return producer


def get_producer_json():
    return producerJson


async def stop():
    global producer, producerJson
    if producer:
        await producer.stop()
    if producerJson:
        await producerJson.stop()
    producer = None
    producerJson = None
