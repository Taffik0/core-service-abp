from src.kafka_producer import get_producer_json

from src.database.class_db import get_class_by_ref
from src.database import user_db_obj
from src.models.users import Student


class ClassRefService:
    async def send_join_to_class(self, user: Student):
        producer = get_producer_json()
        data = {"uuid": str(user.uuid),
                "class_id": user.class_id,
                "class_num": user.class_num,
                "school_id": user.school_id,
                }
        print(f"send {data=}")
        await producer.send("join-to-class", data)
