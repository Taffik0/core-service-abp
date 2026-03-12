from uuid import UUID

from src.services.use_case.join_to_class_use_case import JoinToClassUseCase
from src.database.repository.class_repository import ClassRepository
from src.database.repository.users_schools_ref_repository import UsersSchoolsRefRepository

from src.logger import logger


class JoinToClassByRefUseCase:
    def __init__(self, join_to_class_use_case: JoinToClassUseCase,
                 class_repo: ClassRepository,
                 users_schools_ref_repo: UsersSchoolsRefRepository):
        self.join_to_class_use_case = join_to_class_use_case
        self.class_repo = class_repo
        self.users_schools_ref_repo = users_schools_ref_repo

    async def join(self, user_uuid: UUID, ref: str):
        class_data = await self.class_repo.get_class_by_ref(ref)
        if not await self.users_schools_ref_repo.get_user_school_ref(user_uuid, class_data.school_id):
            await self.users_schools_ref_repo.create_user_school_ref(user_uuid, class_data.school_id)
        await self.join_to_class_use_case.join(user_uuid, class_data.id)
        logger.info("join to class by ref", {"user": user_uuid, "ref": ref, "class_id": class_data.id})
