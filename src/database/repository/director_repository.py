from uuid import UUID
from src.database.dbmanager import get_pool

from src.models.user.user_types import DirectorType
from src.models.user.user_type_update import DirectorTypeUpdate

from asyncpg import Connection, UniqueViolationError


class DirectorRepository:
    async def create_director(self, user_uuid: UUID, director_data: DirectorType, conn: Connection | None = None):
        pass

    async def get_director(self, user_uuid: UUID) -> DirectorType | None:
        pass

    async def delete_director(self, user_uuid: UUID):
        pass

    async def update_director(self, user_uuid: UUID, director_data: DirectorTypeUpdate):
        pass


class DirectorRepositoryPG(DirectorRepository):
    async def create_director(self, user_uuid: UUID, director_data: DirectorType, conn: Connection | None = None):
        if conn:
            return await self._create_director(user_uuid, director_data, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._create_director(user_uuid, director_data, conn)

    async def _create_director(self, user_uuid: UUID, director_data: DirectorType, conn: Connection) -> bool:
        query = """INSERT INTO "director_type" (user_uuid) VALUES($1)"""
        try:
            result = await conn.execute(query, user_uuid)
            return int(result.split()[1]) > 0
        except UniqueViolationError as e:
            return False

    async def get_director(self, user_uuid: UUID) -> DirectorType | None:
        query = """SELECT * FROM "director_type" WHERE user_uuid = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            director_record = await conn.fetchrow(query, user_uuid)
        if not director_record:
            return None
        return DirectorType()

    async def delete_director(self, user_uuid: UUID):
        query = """DELETE FROM "director_type" WHERE user_uuid = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            await conn.execute(query, user_uuid)



