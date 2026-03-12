from aiokafka import ConsumerRecord

from fastapi import Depends

from .message_handler import MessageHandler
from ...logger import logger

from src.services.use_case.user_model_factory import UserInModelFactory
from src.mappers.user_mapper import map_user
from src.services.use_case.create_user_use_case import CreateUserUseCase


class UserRegHandler(MessageHandler):
    _topic = "user-registration"

    def __init__(self, create_user_use_case: CreateUserUseCase, topic: str | None = ""):
        super().__init__(topic)
        self.create_user_use_case = create_user_use_case

    async def process_message(self, msg: ConsumerRecord):
        data: dict | None = msg.value if isinstance(msg.value, dict) else None
        if not isinstance(msg.value, dict):
            logger.warning("Invalid message format")
            return

        logger.info("User registration event received", extra={"payload": data})

        user_in = UserInModelFactory().create_user_model_in(data)
        if user_in is None:
            return
        user = map_user(user_in)
        logger.info(user)
        logger.info(f"start creating")
        await self.create_user_use_case.create_user(user)


