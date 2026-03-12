import asyncio
import json

from aiokafka import AIOKafkaConsumer
from aiokafka.structs import ConsumerRecord

from .message_handlers.message_handler import MessageHandler
from ..logger import logger

STANDARD_DELAY = 5
MAX_DELAY = 30
delay = STANDARD_DELAY


class KafkaListener:
    def __init__(self, group_id: str, message_handlers: list[MessageHandler], bootstrap_servers: str):
        self.group_id = group_id
        self.message_handlers: dict[str, MessageHandler] = {msg_handler.get_topic(): msg_handler
                                                            for msg_handler in message_handlers}
        self.topics = [msg_handler.get_topic() for msg_handler in message_handlers]
        self.bootstrap_servers = bootstrap_servers

    async def consume(self):
        global delay
        while True:
            try:
                logger.info(f"try connect to {self.bootstrap_servers}")

                consumer = AIOKafkaConsumer(
                    *self.topics,
                    bootstrap_servers=self.bootstrap_servers,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    auto_offset_reset='earliest',
                    enable_auto_commit=False,
                    group_id=self.group_id
                )

                logger.info("kafka_listener - started")
                break
            except Exception as e:
                logger.warning(f"can't connect to kafka. Failed by {e}")
                delay *= 1.4
                if delay >= MAX_DELAY:
                    delay = MAX_DELAY
                await asyncio.sleep(delay)

        # Запускаем консьюмера
        await consumer.start()
        try:
            async for msg in consumer:
                handler = self.message_handlers.get(msg.topic)
                if not handler:
                    logger.warning(f"No handler for topic {msg.topic}")
                    continue

                try:
                    await handler.process_message(msg)
                    await consumer.commit()
                except Exception as e:
                    logger.exception("Message processing failed")
                    print(e)

        finally:
            await consumer.stop()