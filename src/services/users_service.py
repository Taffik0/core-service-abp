from dataclasses import dataclass
from uuid import UUID

from src.database.repository.user_repository import UserRepository
from src.models.user.user_types import UserBaseType
from src.models.user.user_type_update import UserBaseTypeUpdate


@dataclass
class UserPublicDTO:
    uuid: UUID
    nickname: str
    firstname: str
    surname: str
    thirdname: str


@dataclass
class UserUpdateDTO:
    nickname: str | None
    firstname: str | None
    surname: str | None
    thirdname: str | None


class UsersService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def _base_type_to_public_dto(self, user: UserBaseType) -> UserPublicDTO:
        return UserPublicDTO(uuid=user.uuid,
                             nickname=user.nickname,
                             firstname=user.firstname,
                             surname=user.surname,
                             thirdname=user.thirdname)

    async def get_user(self, uuid: UUID) -> UserPublicDTO:
        user_db = await self.user_repository.get_user(user_uuid=uuid)
        return self._base_type_to_public_dto(user_db)

    async def get_users_by_uuids(self, uuids: list[UUID], limit: int = 100) -> list[UserPublicDTO]:
        if len(uuids) > limit:
            return []
        users_db = await self.user_repository.get_users_by_uuids(user_uuids=uuids)
        return [self._base_type_to_public_dto(user_db) for user_db in users_db]

    async def update_user(self, user_uuid: UUID, user_update: UserUpdateDTO):
        user_update_bd = UserBaseTypeUpdate(nickname=user_update.nickname,
                           firstname=user_update.firstname,
                           surname=user_update.surname)
        await self.user_repository.update_user(user_uuid=user_uuid, user_data=user_update_bd)

