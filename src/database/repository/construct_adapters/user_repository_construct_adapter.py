from asyncpg import Connection
from uuid import UUID

from src.database.repository.user_repository import UserRepository
from src.models.user.user_type_update import UserBaseTypeUpdate
from src.models.user.user_types import UserBaseType


class UserRepositoryConstructAdapter:
    async def get_user(self, user_uuid: UUID) -> UserBaseType | None:
        pass

    async def update_user(self, user_uuid: UUID, user_data: UserBaseTypeUpdate) -> bool:
        pass

    async def get_users_by_uuids(self, user_uuids: list[UUID]) -> list[UserBaseType]:
        pass


class UserRepositoryConstructAdapterPG(UserRepositoryConstructAdapter):
    def __init__(self, conn: Connection, user_repo: UserRepository):
        self.conn = conn
        self.user_repo = user_repo

    async def get_user(self, user_uuid: UUID) -> UserBaseType | None:
        return await self.user_repo.get_user(user_uuid, conn=self.conn)

    async def update_user(self, user_uuid: UUID, user_data: UserBaseTypeUpdate) -> bool:
        return await self.user_repo.update_user(user_uuid, user_data, conn=self.conn)

    async def get_users_by_uuids(self, user_uuids: list[UUID]) -> list[UserBaseType]:
        return await self.user_repo.get_users_by_uuids(user_uuids, conn=self.conn)