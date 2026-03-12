from uuid import UUID

from src.database.repository.users_classes_ref_repository import UsersClassesRefRepository
from src.database.repository.student_repository import StudentRepository
from src.database.repository.class_repository import ClassRepository

from src.clients.kafka.join_to_class_event_client import JoinToClassEventClient

from src.logger import logger


class JoinToClassUseCase:
    def __init__(self, users_classes_ref_repo: UsersClassesRefRepository,
                 student_repo: StudentRepository,
                 class_repo: ClassRepository,
                 join_to_class_event_client: JoinToClassEventClient):
        self.users_classes_ref_repo = users_classes_ref_repo
        self.student_repo = student_repo
        self.class_repo = class_repo
        self.join_to_class_event_client = join_to_class_event_client

    async def join(self, user_uuid: UUID, class_id: int) -> bool:
        ref_id = await self.users_classes_ref_repo.create_ref(user_uuid, class_id)
        if ref_id is None:
            logger.info(f"join to class failed, ref not created",
                        {"user_uuid": user_uuid, "class_id": class_id})
            return False
        if await self.student_repo.get_student(user_uuid):
            class_data = await self.class_repo.get_class_by_id(class_id)
            await self.join_to_class_event_client.send_message(
                user_uuid,
                class_id,
                class_data.class_num,
                class_data.school_id)
        logger.info(f"join to class",
                    {"user_uuid": user_uuid, "class_id": class_id})
        return True
