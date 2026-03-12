from uuid import UUID
from dataclasses import dataclass
from typing import TYPE_CHECKING


from asyncpg import Connection

from src.database.dbmanager import get_pool


@dataclass
class UserSchoolDBDTO:
    id: int
    user_uuid: UUID
    school_id: int


class UsersSchoolsRefRepository:
    async def create_user_school_ref(self, user_uuid: UUID, school_id: int,
                                     conn: Connection | None = None) -> int:
        pass

    async def delete_user_school_ref(self, user_uuid: UUID, school_id: int,
                                     conn: Connection | None = None):
        pass

    async def delete_user_school_ref_by_id(self, user_school_ref_id: int,
                                           conn: Connection | None = None):
        pass

    async def delete_all_user_school_ref(self, user_uuid: UUID,
                                         conn: Connection | None = None):
        pass

    async def get_all_user_school_ref(self, user_uuid: UUID,
                                      conn: Connection | None = None) -> list[UserSchoolDBDTO]:
        pass

    async def get_user_school_ref(self, user_uuid: UUID, school_id: int,
                                  conn: Connection | None = None) -> UserSchoolDBDTO | None:
        pass

    async def get_user_school_ref_by_id(self, user_school_ref_id: int,
                                        conn: Connection | None = None) -> UserSchoolDBDTO | None:
        pass


class UsersSchoolsRefRepositoryPG(UsersSchoolsRefRepository):

    def _record_to_dto(self, record) -> UserSchoolDBDTO:
        return UserSchoolDBDTO(
            id=record["id"],
            school_id=record["school_id"],
            user_uuid=record["user_uuid"])

    def _records_to_dtos(self, records) -> list[UserSchoolDBDTO]:
        return [
            self._record_to_dto(r)
            for r in records
        ]

    async def create_user_school_ref(self, user_uuid: UUID, school_id: int,
                                      conn: Connection | None = None) -> int:
        if conn:
            return await self._create_user_school_ref(user_uuid, school_id, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._create_user_school_ref(user_uuid, school_id, conn)

    async def _create_user_school_ref(self, user_uuid: UUID, school_id: int, conn: Connection) -> int:
        query = """INSERT INTO users_schools_ref (user_uuid, school_id) VALUES ($1, $2) RETURNING id"""
        ref_id = await conn.fetchrow(query, user_uuid, school_id)
        return ref_id["id"]

    async def get_all_user_school_ref(self, user_uuid: UUID,
                                      conn: Connection | None = None) -> list[UserSchoolDBDTO]:
        if conn:
            return await self._get_all_user_school_ref(user_uuid, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._get_all_user_school_ref(user_uuid, conn)

    async def _get_all_user_school_ref(self, user_uuid: UUID, conn: Connection) -> list[UserSchoolDBDTO]:
        query = """SELECT id, user_uuid, school_id FROM users_schools_ref WHERE user_uuid = $1"""
        user_schools_refs_records = await conn.fetch(query, user_uuid)
        return self._records_to_dtos(user_schools_refs_records)

    async def get_user_school_ref(self, user_uuid: UUID, school_id: int,
                                  conn: Connection | None = None) -> UserSchoolDBDTO | None:
        if conn:
            return await self._get_user_school_ref(user_uuid, school_id, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._get_user_school_ref(user_uuid, school_id, conn)

    async def _get_user_school_ref(self, user_uuid: UUID, school_id: int, conn: Connection) -> UserSchoolDBDTO | None:
        query = """SELECT id, user_uuid, school_id FROM users_schools_ref 
        WHERE user_uuid = $1 AND school_id = $2"""
        record = await conn.fetchrow(query, user_uuid, school_id)
        if not record:
            return None
        return self._record_to_dto(record)

    async def get_user_school_ref_by_id(self, user_school_ref_id: int,
                                        conn: Connection | None = None) -> UserSchoolDBDTO | None:
        if conn:
            return await self._get_user_school_ref_by_id(user_school_ref_id, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._get_user_school_ref_by_id(user_school_ref_id, conn)

    async def _get_user_school_ref_by_id(self, user_school_ref_id: int, conn: Connection) -> UserSchoolDBDTO | None:
        query = """SELECT id, user_uuid, school_id FROM users_schools_ref 
        WHERE id = $1"""
        record = await conn.fetchrow(query, user_school_ref_id)
        if not record:
            return None
        return self._record_to_dto(record)

    async def delete_user_school_ref(self, user_uuid: UUID, school_id: int, conn: Connection | None = None):
        if conn:
            return await self._delete_user_school_ref(user_uuid, school_id, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._delete_user_school_ref(user_uuid, school_id, conn)

    async def _delete_user_school_ref(self, user_uuid: UUID, school_id: int, conn: Connection):
        query = """DELETE FROM users_schools_ref 
        WHERE user_uuid = $1 AND school_id = $2"""
        await conn.execute(query, user_uuid, school_id)

    async def delete_all_user_school_ref(self, user_uuid: UUID, conn: Connection | None = None):
        if conn:
            return await self._delete_all_user_school_ref(user_uuid, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._delete_all_user_school_ref(user_uuid, conn)

    async def _delete_all_user_school_ref(self, user_uuid: UUID, conn: Connection):
        query = """DELETE FROM users_schools_ref 
        WHERE user_uuid = $1"""
        await conn.execute(query, user_uuid)

    async def delete_user_school_ref_by_id(self, user_school_ref_id: int, conn: Connection | None = None):
        if conn:
            return await self._delete_user_school_ref_by_id(user_school_ref_id, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._delete_user_school_ref_by_id(user_school_ref_id, conn)

    async def _delete_user_school_ref_by_id(self, user_school_ref_id: int, conn: Connection):
        query = """DELETE FROM users_schools_ref 
        WHERE id = $1"""
        await conn.execute(query, user_school_ref_id)

