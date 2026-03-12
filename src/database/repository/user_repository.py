from uuid import UUID

from asyncpg import Connection, UniqueViolationError

from src.database.dbmanager import get_pool

from src.models.user.user_types import UserBaseType
from src.models.user.user_type_update import UserBaseTypeUpdate


class UserRepository:
    async def get_user(self, user_uuid: UUID, conn: Connection | None = None) -> UserBaseType:
        pass

    async def create_user(self, user_base: UserBaseType, conn: Connection | None = None):
        pass

    async def update_user(self, user_uuid: UUID, user_data: UserBaseTypeUpdate, conn: Connection | None = None) -> bool:
        pass

    async def get_users_by_uuids(self, user_uuids: list[UUID], conn: Connection | None = None) -> list[UserBaseType]:
        pass


class UserRepositoryPG(UserRepository):

    def _to_user_obj(self, record) -> UserBaseType:
        return UserBaseType(
            uuid=record["uuid"],
            firstname=record["firstname"],
            surname=record["surname"],
            thirdname=record["thirdname"],
            nickname=record["nickname"],
            type=record["type"])

    async def create_user(self, user_base: UserBaseType, conn: Connection | None = None) -> bool:
        if conn:
            return await self._create_user(user_base, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._create_user(user_base, conn)

    async def _create_user(self, user_base: UserBaseType, conn: Connection) -> bool:
        query = """INSERT INTO "users" 
        (uuid, firstname, 
        surname, thirdname, 
        nickname, type)
        VALUES ($1, $2, $3, $4, $5, $6)"""
        uuid = user_base.uuid
        firstname = user_base.firstname
        surname = user_base.surname
        thirdname = user_base.thirdname
        nickname = user_base.nickname
        user_type = user_base.type
        try:
            result = await conn.execute(query,
                               uuid, firstname,
                               surname, thirdname,
                               nickname, user_type)
        except UniqueViolationError as e:
            return False
        return int(result.split()[2]) > 0

    async def get_user(self, user_uuid: UUID, conn: Connection | None = None) -> UserBaseType | None:
        if conn:
            return await self._get_user(user_uuid, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._get_user(user_uuid, conn)

    async def _get_user(self, user_uuid: UUID, conn: Connection) -> UserBaseType | None:
        query = """
        SELECT 
            uuid, firstname, 
            surname, thirdname, 
            nickname, type
        FROM "users"
        WHERE uuid = $1
        """
        record = await conn.fetchrow(query, user_uuid)
        if not record:
            return None
        return self._to_user_obj(record)

    async def update_user(self, user_uuid: UUID, user_data: UserBaseTypeUpdate,
                           conn: Connection | None = None) -> bool:
        if conn:
            return await self._update_user(user_uuid, user_data, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._update_user(user_uuid, user_data, conn)

    async def _update_user(self, user_uuid: UUID, user_data: UserBaseTypeUpdate, conn: Connection) -> bool:
        fields = []
        values = []
        idx = 2

        for field, value in user_data.__dict__.items():
            if value is None:
                continue
            fields.append(f"{field} = ${idx}")
            values.append(value)
            idx += 1

        if not fields:
            return False

        query = f"""
            UPDATE "users"
            SET {", ".join(fields)}
            WHERE uuid = $1
        """

        result = await conn.execute(query, user_uuid, *values)

        return result != "UPDATE 0"

    async def get_users_by_uuids(self, user_uuids: list[UUID], conn: Connection| None = None) -> list[UserBaseType]:
        if conn:
            return await self._get_users_by_uuids(user_uuids, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._get_users_by_uuids(user_uuids, conn)

    async def _get_users_by_uuids(self, user_uuids: list[UUID], conn: Connection) -> list[UserBaseType]:
        query = """
        SELECT uuid, firstname, surname, thirdname, nickname, type
        FROM "users"
        WHERE uuid = ANY($1::uuid[])
        """
        rows = await conn.fetch(query, user_uuids)
        return [self._to_user_obj(row) for row in rows]