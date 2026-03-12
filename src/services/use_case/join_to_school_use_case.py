from typing import TYPE_CHECKING
from uuid import UUID

from src.database.repository.users_schools_ref_repository import UsersSchoolsRefRepository

from asyncpg import Connection

from src.logger import logger


class JoinToSchoolUseCase:
    def __init__(self, users_schools_ref_repository: UsersSchoolsRefRepository):
        self.users_schools_ref_repository = users_schools_ref_repository

    async def join_to_school(self, user_uuid: UUID, school_id: int, conn: Connection | None = None) -> bool:
        is_exist = await self.users_schools_ref_repository.get_user_school_ref(user_uuid, school_id)
        if not is_exist:
            ref_id: int = await self.users_schools_ref_repository.create_user_school_ref(user_uuid,
                                                                                         school_id, conn=conn)
            logger.info(f"join ${user_uuid} to {school_id}")
            return ref_id is not None
        logger.info(f"failed join  ${user_uuid} to {school_id}; ref is exist {is_exist}")
        return False
