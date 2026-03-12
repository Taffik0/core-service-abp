from uuid import UUID

from src.logger import logger

from src.kafka_producer import get_producer_json


class JoinToClassEventClient:
    async def send_message(self, user_uuid: UUID, class_id: int, class_num: int, school_id: int):
        await get_producer_json().send(
            "join-to-class",
            {"user_uuid": user_uuid,
             "class_id": class_id,
             "class_num": class_num,
             "school_id": school_id})
        logger.info("send message (join-to-class)",
                    {"user_uuid": user_uuid,
                     "class_id": class_id,
                     "class_num": class_num,
                     "school_id": school_id})
