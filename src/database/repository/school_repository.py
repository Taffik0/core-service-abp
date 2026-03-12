from dataclasses import dataclass
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from asyncpg import Connection

from src.database.dbmanager import get_pool
from src.models.dto.school_db_dto import SchoolDBDTO, SchoolEntryRequestsDTO


class SchoolRepository:
    async def get_school_of_user(self, user_uuid: UUID, count: int | None = None, start: int = 0) -> list[SchoolDBDTO]:
        pass

    async def get_school(self, school_id: int) -> SchoolDBDTO | None:
        pass

    async def get_schools(self, count: int, start: int = 0) -> list[SchoolDBDTO]:
        pass

    async def create_school(self, name: str, description: str) -> int:
        """return id"""
        pass

    async def set_ref(self, school_id: int, ref: str | None):
        pass

    async def get_school_by_ref(self, school_ref) -> SchoolDBDTO | None:
        pass

    async def get_school_entry_requests(self, school_id: int) -> list[SchoolEntryRequestsDTO]:
        pass

    async def get_school_entry_request(self, request_id: int) -> SchoolEntryRequestsDTO | None:
        pass

    async def delete_school_entry_request(self, request_id: int):
        pass

    async def create_school_entry_request(self, user_uuid: UUID, school_id: int) -> int:
        pass

    async def change_school(self, school_id: int, name: str | None, description: str | None):
        pass

    async def delete_school(self, school_id: int):
        pass


class SchoolRepositoryPG(SchoolRepository):
    async def get_school(self, school_id: int) -> SchoolDBDTO | None:
        query = """
            SELECT 
                id, name, 
                description, ref 
            FROM schools 
            WHERE id = $1
        """
        async with get_pool().acquire() as conn:  # type: Connection
            school_record = await conn.fetchrow(query, school_id)
            if not school_record:
                return None
            return SchoolDBDTO(id=school_record["id"],
                               name=school_record["name"],
                               description=school_record["description"],
                               ref=school_record["ref"])

    async def get_schools(self, count: int, start: int = 0) -> list[SchoolDBDTO]:
        query = """
            SELECT 
                id, name, 
                description, ref 
            FROM schools 
            LIMIT $2 OFFSET $3
        """
        async with get_pool().acquire() as conn:  # type: Connection
            schools_records = await conn.fetch(query, count, start)

        return [
            SchoolDBDTO(
                id=record["id"],
                name=record["name"],
                description=record["description"],
                ref=record["ref"]
            )
            for record in schools_records
        ]

    async def get_school_of_user(self, user_uuid: UUID, count: int | None = None, start: int = 0) -> list[SchoolDBDTO]:
        params = [user_uuid, start]
        limit_sql = ""

        if count is not None:
            params.append(count)
            limit_sql = "FETCH NEXT $3 ROWS ONLY"
        query = f"""
            SELECT 
                sc.id, sc.name, 
                sc.description, sc.ref
            FROM "users_schools_ref" AS sr
            JOIN "schools" AS sc ON sc.id = sr.school_id
            WHERE sr.user_uuid = $1
            ORDER BY sc.id
            OFFSET $2 ROWS
            {limit_sql}
        """

        async with get_pool().acquire() as conn:  # type: Connection
            schools_records = await conn.fetch(query, *params)

        return [
            SchoolDBDTO(
                id=record["id"],
                name=record["name"],
                description=record["description"],
                ref=record["ref"]
            )
            for record in schools_records
        ]

    async def create_school(self, name: str, description: str) -> int:
        query = """INSERT INTO "schools" (name, description) VALUES ($1, $2) RETURNING id"""

        async with get_pool().acquire() as conn:  # type: Connection
            school_id = await conn.fetchrow(query, name, description)
        return school_id["id"]

    async def set_ref(self, school_id: int, ref: str | None):
        query = """UPDATE "schools" SET ref = $2 WHERE id = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            await conn.execute(query, school_id, ref)
            
    async def get_school_by_ref(self, school_ref) -> SchoolDBDTO | None:
        query = "SELECT id, name, description, ref FROM schools WHERE ref = $1"
        async with get_pool().acquire() as conn:  # type: Connection
            school_record = await conn.fetchrow(query, school_ref)

        if not school_record:
            return None
        
        return SchoolDBDTO(id=school_record["id"],
                           name=school_record["name"],
                           description=school_record["description"],
                           ref=school_record["ref"])

    async def get_school_entry_requests(self, school_id: int) -> list[SchoolEntryRequestsDTO]:
        query = """SELECT id, user_uuid, school_if FROM school_entry_requests WHERE id = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            request_records = await conn.fetchrow(query, school_id)
        return [
            SchoolEntryRequestsDTO(
                id=record["id"],
                user_uuid=record["user_uuid"],
                school_id=record["school_id"]
            )
            for record in request_records
        ]

    async def get_school_entry_request(self, request_id: int) -> SchoolEntryRequestsDTO | None:
        query = """SELECT id, user_uuid, school_if FROM school_entry_requests WHERE id = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            record = await conn.fetchrow(query, request_id)
        if not record:
            return None
        return SchoolEntryRequestsDTO(
            id=record["id"],
            user_uuid=record["user_uuid"],
            school_id=record["school_id"]
        )

    async def create_school_entry_request(self, user_uuid: UUID, school_id: int) -> int:
        query = """INSERT INTO school_entry_requests (user_uuid, school_id) VALUES($1, $2)"""
        async with get_pool().acquire() as conn:  # type: Connection
            record = await conn.fetchrow(query, user_uuid, school_id)
        return record["id"]

    async def delete_school_entry_request(self, request_id: int):
        query = """DELETE FROM school_entry_requests WHERE id = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            await conn.execute(query, request_id)

    async def change_school(self, school_id: int, name: str | None, description: str | None):
        fields = []
        values = []
        idx = 2  # $1 уже занят school_id

        if name is not None:
            fields.append(f"name = ${idx}")
            values.append(name)
            idx += 1
        if description is not None:
            fields.append(f"description = ${idx}")
            values.append(description)
            idx += 1

        if not fields:
            return  # нечего обновлять

        query = f'UPDATE "schools" SET {", ".join(fields)} WHERE id = $1'

        async with get_pool().acquire() as conn:
            await conn.fetchrow(query, school_id, *values)

    async def delete_school(self, school_id: int):
        query = f'DELETE FROM "schools" WHERE id = $1'
        async with get_pool().acquire() as conn:  # type: Connection
            await conn.fetchrow(query, school_id)
