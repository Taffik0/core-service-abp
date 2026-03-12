from uuid import UUID
from src.database.dbmanager import get_pool

from src.models.user.user_types import StudentType

from asyncpg import Connection, UniqueViolationError


class StudentRepository:
    async def create_student(self, user_uuid: UUID, student_data: StudentType, conn: Connection | None = None) -> bool:
        pass

    async def get_student(self, user_uuid: UUID) -> StudentType | None:
        pass

    async def delete_user(self, user_uuid: UUID) -> bool:
        pass

    async def update_student(self, user_uuid: UUID, data: StudentType) -> bool:
        pass


class StudentRepositoryPG(StudentRepository):
    async def create_student(self, user_uuid: UUID, student_data: StudentType, conn: Connection | None = None) -> bool:
        if conn:
            return await self._create_student(user_uuid, student_data, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._create_student(user_uuid, student_data, conn)

    async def _create_student(self, user_uuid: UUID, student_data: StudentType, conn: Connection) -> bool:
        query = """INSERT INTO "student_type" (user_uuid, class_id, class_num) VALUES ($1, $2, $3)"""
        try:
            result = await conn.execute(query, user_uuid, student_data.class_id, student_data.class_num)
        except UniqueViolationError:
            return False
        return int(result.split()[2]) > 0

    async def get_student(self, user_uuid: UUID) -> StudentType | None:
        query = """SELECT user_uuid, class_id, class_num FROM "student_type" WHERE user_uuid = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            record = await conn.fetchrow(query, user_uuid)

        if not record:
            return None
        return StudentType(class_id=record["class_id"], class_num=record["class_num"], user_uuid=record["user_uuid"])

    async def delete_user(self, user_uuid: UUID):
        query = """DELETE FROM "student_type" WHERE user_uuid = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            result = await conn.execute(query, user_uuid)
        return result != "UPDATE 0"

    async def update_student(self, user_uuid: UUID, data: StudentType) -> bool:
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
            UPDATE "student_type"
            SET {", ".join(fields)}
            WHERE user_uuid = $1
        """

        async with get_pool().acquire() as conn:   # type: Connection
            result = await conn.execute(query, user_uuid, *values)

        return result != "UPDATE 0"
