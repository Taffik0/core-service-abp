from asyncpg import Connection

from dataclasses import dataclass
from uuid import UUID

from src.database.dbmanager import get_pool
from src.models.user.user_type_enum import UserTypes


@dataclass
class UsersSchoolRefDBDTO:
    id: int
    user_uuid: UUID
    class_id: int


class UsersClassesRefRepository:
    async def create_ref(self, user_uuid: UUID, class_id: int) -> int | None:
        pass

    async def get_refs_of_class(self, class_id: int) -> list[UsersSchoolRefDBDTO]:
        pass

    async def get_refs_of_user(self, user_uuid: UUID) -> list[UsersSchoolRefDBDTO]:
        pass

    async def get_refs_of_user_and_school(self, user_uuid: UUID, school_id: int) -> list[UsersSchoolRefDBDTO]:
        pass

    async def get_ref(self, user_uuid: UUID, class_id: int) -> UsersSchoolRefDBDTO | None:
        pass

    async def delete_ref(self, user_uuid: UUID, class_id: int):
        pass

    async def delete_ref_of_user_and_school(self, user_uuid: UUID, school_id: int):
        pass

    async def get_joint_class(self, user1_uuid: UUID, user2_uuid: UUID) -> list[int]:
        pass

    async def get_refs_of_class_by_role(self, class_id: int, user_role: UserTypes) -> list[UsersSchoolRefDBDTO]:
        pass


class UsersClassesRefRepositoryPG(UsersClassesRefRepository):
    def _to_ref_dto(self, record) -> UsersSchoolRefDBDTO:
        return UsersSchoolRefDBDTO(id=record["id"],
                                   user_uuid=record["user_uuid"],
                                   class_id=record["class_id"])

    async def create_ref(self, user_uuid: UUID, class_id: int) -> int | None:
        query = """
        INSERT INTO users_classes_ref (user_uuid, class_id, school_ref_id)
        SELECT
            $1,
            c.id,
            usr.id
        FROM classes AS c
        JOIN users_schools_ref AS usr
            ON usr.school_id = c.school_id
           AND usr.user_uuid = $1
        WHERE c.id = $2
        RETURNING id;
        """

        async with get_pool().acquire() as conn:
            record = await conn.fetchrow(query, user_uuid, class_id)

        if record is None:
            return None

        return record["id"]

    async def get_refs_of_class(self, class_id: int) -> list[UsersSchoolRefDBDTO]:
        query = """SELECT id, user_uuid, class_id FROM users_classes_ref WHERE class_id = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            records = await conn.fetch(query, class_id)
        return [self._to_ref_dto(record) for record in records]

    async def get_refs_of_user(self, user_uuid: UUID) -> list[UsersSchoolRefDBDTO]:
        query = """SELECT id, user_uuid, class_id FROM users_classes_ref WHERE user_uuid = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            records = await conn.fetch(query, user_uuid)
        return [self._to_ref_dto(record) for record in records]

    async def get_refs_of_user_and_school(self, user_uuid: UUID, school_id: int) -> list[UsersSchoolRefDBDTO]:
        query = """
        SELECT ucr.id, ucr.user_uuid, ucr.class_id FROM "classes" AS c
        JOIN users_classes_ref as ucr ON c.id = ucr.class_id
        WHERE c.school_id = $1 AND ucr.user_uuid = $2"""
        async with get_pool().acquire() as conn:  # type: Connection
            records = await conn.fetch(query, school_id, user_uuid)
        return [self._to_ref_dto(record) for record in records]

    async def get_ref(self, user_uuid: UUID, class_id: int) -> UsersSchoolRefDBDTO | None:
        query = """
        SELECT id, user_uuid, class_id 
        FROM users_classes_ref 
        WHERE user_uuid = $1 AND class_id = $2"""
        async with get_pool().acquire() as conn:  # type: Connection
            record = await conn.fetchrow(query, user_uuid, class_id)
        if record is None:
            return None
        return self._to_ref_dto(record)

    async def delete_ref(self, user_uuid: UUID, class_id: int):
        query = """DELETE FROM users_classes_ref WHERE user_uuid = $1 AND class_id = $2"""
        async with get_pool().acquire() as conn:  # type: Connection
            response = await conn.execute(query, user_uuid, class_id)

    async def delete_ref_of_user_and_school(self, user_uuid: UUID, school_id: int):
        query = """
        DELETE FROM users_classes_ref ucr
        USING classes c
        WHERE ucr.class_id = c.id
          AND c.school_id = $1
          AND ucr.user_uuid = $2;
        """
        async with get_pool().acquire() as conn:  # type: Connection
            response = await conn.execute(query, school_id, user_uuid)

    async def get_joint_class(self, user1_uuid: UUID, user2_uuid: UUID) -> list[int]:
        query = """
        SELECT class_id
        FROM users_classes_ref
        WHERE user_uuid = $1
        
        INTERSECT
        
        SELECT class_id
        FROM users_classes_ref
        WHERE user_uuid = $2;
        ORDER BY class_id;
        """
        async with get_pool().acquire() as conn:  # type: Connection
            records = await conn.fetch(query, user1_uuid, user2_uuid)
        return [record["class_id"] for record in records]

    async def get_refs_of_class_by_role(self, class_id: int, user_role: UserTypes) -> list[UsersSchoolRefDBDTO]:
        query = """
        SELECT ucr.id, ucr.user_uuid, ucr.class_id
        FROM users_classes_ref ucr
        JOIN users u ON u.uuid = ucr.user_uuid
        WHERE ucr.class_id = $1
          AND u.type = $2;"""
        async with get_pool().acquire() as conn:  # type: Connection
            records = await conn.fetch(query, class_id, user_role.value)
        return [self._to_ref_dto(record) for record in records]
