import asyncio

from src.conf.urls import BROKER_URL

from .kafka_listaner import KafkaListener
from .message_handlers.user_reg_handler import UserRegHandler

from src.dependencies.user_dependecies import build_create_user_use_case


GROUP_ID = "user-data-service"
BOOTSTRAP_SERVICE = BROKER_URL

KAFKA_LISTENERS = [KafkaListener(GROUP_ID, [UserRegHandler(build_create_user_use_case())], BOOTSTRAP_SERVICE)]
kafka_tasks = []


async def init():
    for kafka_listener in KAFKA_LISTENERS:
        kafka_task = asyncio.create_task(kafka_listener.consume())
        kafka_tasks.append(kafka_task)


async def stop():
    for kafka_task in kafka_tasks:
        kafka_task.cancel()
        try:
            await kafka_task
        except asyncio.CancelledError:
            pass
