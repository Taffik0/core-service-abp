from dataclasses import dataclass
from uuid import UUID
from src.database import dbmanager
from src.database.dbmanager import get_pool

from src.models.user.user_types import TeacherType
from src.models.user.user_type_update import TeacherTypeUpdate

from asyncpg import Connection, UniqueViolationError


@dataclass
class ClassDTO:
    id: int
    school_id: int
    class_ref: str
    class_num: int
    name: str


class TeacherRepository:
    async def get_teacher(self, uuid: UUID) -> TeacherType | None:
        """None сли такого учителя нет или пользователь не учитель"""
        pass

    async def crate_teacher_type(self, user_uuid: UUID, teacher_type: TeacherType,
                                 conn: Connection | None = None) -> int | None:
        pass

    async def get_teacher_classes(self, uuid: UUID) -> list[ClassDTO]:
        pass

    async def get_teacher_classes_id(self, uuid: UUID) -> list[int]:
        pass

    async def update_teacher(self, user_uuid: UUID, data: TeacherTypeUpdate):
        pass


class TeacherRepositoryPG(TeacherRepository):
    async def get_teacher(self, uuid: UUID) -> TeacherType | None:
        query = """
            SELECT id, user_uuid, subject_id 
            FROM teacher_type 
            WHERE user_uuid = $1
        """
        async with get_pool().acquire() as conn:  # type: Connection
            teacher_record = await conn.fetchrow(query, uuid)
        if not teacher_record:
            return None
        return TeacherType(id=teacher_record["id"],
                           user_uuid=teacher_record["user_uuid"],
                           subject_id=teacher_record["subject_id"])

    async def get_teacher_classes(self, uuid: UUID):
        query = """
            SELECT 
                cl.id, 
                cl.school_id, 
                cl.class_ref, 
                cl.class_num, 
                cl.name
            FROM "teacher-to-class"  AS tc
            JOIN "classes" AS cl ON tc.class_id = cl.id
            WHERE tc.teacher_uuid = $1
        """
        async with get_pool().acquire() as conn:  # type: Connection
            class_records = await conn.fetch(query, uuid)
        return [ClassDTO(id=record["id"],
                         school_id=record["school_id"],
                         class_ref=record["class_ref"],
                         class_num=record["class_num"],
                         name=record["name"])
                for record in class_records]

    async def get_teacher_classes_id(self, teacher_uuid: UUID) -> list[int]:
        query = """
            SELECT class_id
            FROM "teacher-to-class"
            WHERE teacher_uuid = $1
        """
        async with dbmanager.db_pool.acquire() as conn:
            records = await conn.fetch(query, teacher_uuid)

        return [r["class_id"] for r in records]

    async def crate_teacher_type(self, user_uuid: UUID, teacher_type: TeacherType,
                                 conn: Connection | None = None) -> int | None:
        if conn:
            return await self._crate_teacher_type(user_uuid, teacher_type, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._crate_teacher_type(user_uuid, teacher_type, conn)

    async def _crate_teacher_type(self, user_uuid: UUID, teacher_type: TeacherType, conn: Connection) -> int | None:
        query = """
            INSERT INTO "teacher_type" 
            (user_uuid, subject_id) 
            VALUES($1, $2)
            RETURNING(id)
        """
        try:
            record = await conn.fetchrow(query, user_uuid, teacher_type.subject_id)
        except UniqueViolationError:
            return None
        return record["id"] if record else None

    async def update_teacher(self, user_uuid: UUID, data: TeacherTypeUpdate) -> bool:
        fields = []
        values = []
        idx = 2

        for field, value in data.__dict__.items():
            if value is None:
                continue
            fields.append(f"{field} = ${idx}")
            values.append(value)
            idx += 1

        if not fields:
            return False

        query = f"""
            UPDATE "teacher_type"
            SET {", ".join(fields)}
            WHERE user_uuid = $1
        """

        async with get_pool().acquire() as conn:   # type: Connection
            result = await conn.execute(query, user_uuid, *values)

        return result != "UPDATE 0"


