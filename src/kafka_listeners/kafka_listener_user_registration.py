import json
from aiokafka import AIOKafkaConsumer
from src.models.user.user_fabric import create_user_by_dict
from src.database.user_db_obj import insert_user

from src.logger import logger

KAFKA_TOPIC = "user-registration"


async def consume(group_id: str, bootstrap_servers: str):
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )
    # запуск потребителя
    await consumer.start()
    logger.info(f"Async consumer started {KAFKA_TOPIC}")
    try:
        async for msg in consumer:
            data = msg.value
            logger.info(f"Получено: {data}")
            try:
                user = create_user_by_dict(data)
                await insert_user(user)
            except Exception as e:
                logger.error(f"Ошибка обработки сообщения: {e}")
    finally:
        await consumer.stop()