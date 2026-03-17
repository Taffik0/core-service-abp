import asyncio
import json

from aiokafka import AIOKafkaConsumer
from aiokafka.structs import ConsumerRecord

from .message_handlers.message_handler import MessageHandler
from ..logger import logger


class KafkaListener:
    def __init__(self, group_id: str, message_handlers: list[MessageHandler], bootstrap_servers: str):
        self.group_id = group_id
        self.message_handlers: dict[str, MessageHandler] = {msg_handler.get_topic(): msg_handler
                                                            for msg_handler in message_handlers}
        self.topics = [msg_handler.get_topic()
                       for msg_handler in message_handlers]
        self.bootstrap_servers = bootstrap_servers


async def consume(self):
    delay = 1

    while True:
        consumer = None
        try:
            logger.info(f"connecting to {self.bootstrap_servers}")

            consumer = AIOKafkaConsumer(
                *self.topics,
                bootstrap_servers=self.bootstrap_servers,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=False,
                group_id=self.group_id
            )

            await consumer.start()
            logger.info("kafka connected")

            delay = 1  # сбрасываем backoff

            async for msg in consumer:
                handler = self.message_handlers.get(msg.topic)

                if not handler:
                    logger.warning(f"No handler for topic {msg.topic}")
                    continue

                try:
                    await handler.process_message(msg)
                    await consumer.commit()

                except Exception:
                    logger.exception("Message processing failed")

        except Exception as e:
            logger.exception(f"kafka consumer crashed: {e}")

        finally:
            if consumer:
                await consumer.stop()

        delay = min(delay * 1.5, 60)
        logger.info(f"reconnecting in {delay} sec")
        await asyncio.sleep(delay)
