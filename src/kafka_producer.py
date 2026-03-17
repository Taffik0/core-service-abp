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
    global producer, producerJson, delay

    while True:
        try:
            producer = AIOKafkaProducer(
                bootstrap_servers=BROKER_URL
            )

            producerJson = AIOKafkaProducer(
                bootstrap_servers=BROKER_URL,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )

            await producer.start()
            await producerJson.start()

            delay = STANDARD_DELAY
            logger.info("Kafka producer started")

            return

        except Exception as e:
            logger.warning(f"can't connect to kafka. Failed by {e}")

            delay = min(delay * 1.5, MAX_DELAY)
            await asyncio.sleep(delay)


async def restart_producer():
    global producer, producerJson

    try:
        if producer:
            await producer.stop()
        if producerJson:
            await producerJson.stop()
    except Exception:
        pass

    await start()


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


async def send_dict(topic: str, data: dict):
    global producerJson

    while True:
        if producerJson is None:
            asyncio.sleep(1)
        try:
            await producer.send_and_wait(topic, data)
            return
        except Exception as e:
            logger.exception("Kafka send failed")

            await restart_producer()
            await asyncio.sleep(2)
