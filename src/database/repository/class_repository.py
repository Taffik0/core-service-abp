from asyncpg import Connection, UniqueViolationError
from uuid import UUID

from src.database.dbmanager import get_pool
from src.models.classes import ClassDBDTO, ClassDBDTO


class ClassRepository:
    async def set_class_to_student(self, class_id: int, user_uuid: str):
        pass

    async def get_classes_of_user(self, user_uuid: UUID) -> list[ClassDBDTO]:
        pass

    async def get_class_by_ref(self, ref: str) -> ClassDBDTO | None:
        pass

    async def get_class_by_id(self, class_id: int) -> ClassDBDTO | None:
        pass

    async def get_classes_of_school(self, school_id: int) -> list[ClassDBDTO]:
        pass

    async def get_classes_of_user_and_school(self, user_uuid: UUID, school_id: int) -> list[ClassDBDTO]:
        pass

    async def create_class(self, school_id: int, name: str, class_num: int) -> int:
        pass

    async def delete_class(self, class_id: int):
        pass


class ClassRepositoryPG(ClassRepository):
    
    def _to_class_dto(self, class_record) -> ClassDBDTO:
        return ClassDBDTO(id=class_record["id"],
                          school_id=class_record["school_id"],
                          class_ref=class_record["class_ref"],
                          class_num=class_record["class_num"],
                          name=class_record["name"])
    
    async def set_class_to_student(self, class_id: int, user_uuid: str):
        async with get_pool().acquire() as conn:
            school_class = await self.get_class_by_id(class_id)
            await conn.execute("""
                UPDATE student_type SET class_id = $1, class_num = $2
                WHERE user_uuid = $3
                """, class_id, school_class.class_num, user_uuid)

    async def get_class_by_ref(self, ref: str) -> ClassDBDTO | None:
        async with get_pool().acquire() as conn:
            class_dict = await conn.fetchrow("""SELECT id ,school_id, class_ref, class_num, name 
                                                FROM classes 
                                                WHERE class_ref = $1""", ref)
            if class_dict:
                return self._to_class_dto(class_dict)
            else:
                return None

    async def get_class_by_id(self, class_id: int) -> ClassDBDTO | None:
        async with get_pool().acquire() as conn:
            class_dict = await conn.fetchrow("""SELECT id ,school_id, class_ref, class_num, name 
                                                FROM classes 
                                                WHERE id = $1""", class_id)
            if class_dict:
                return self._to_class_dto(class_dict)
            else:
                return None

    async def get_classes_of_school(self, school_id: int) -> list[ClassDBDTO]:
        query = """SELECT id ,school_id, class_ref, class_num, name FROM "classes" WHERE school_id = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            records = await conn.fetch(query, school_id)
        return [self._to_class_dto(record) for record in records]

    async def get_classes_of_user(self, user_uuid: UUID) -> list[ClassDBDTO]:
        query = """SELECT c.id ,c.school_id, c.class_ref, c.class_num 
        FROM users_classes_res AS ucr
        JOIN "classes" AS c ON ucr.class_id = c.id
        WHERE ucr.user_uuid = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            records = await conn.fetch(query, user_uuid)
        return [self._to_class_dto(record) for record in records]

    async def get_classes_of_user_and_school(self, user_uuid: UUID, school_id: int) -> list[ClassDBDTO]:
        query = """SELECT c.id ,c.school_id, c.class_ref, c.class_num 
        FROM users_classes_res AS ucr
        JOIN "classes" AS c ON ucr.class_id = c.id
        WHERE ucr.user_uuid = $1 AND c.school_id = $2"""
        async with get_pool().acquire() as conn:  # type: Connection
            records = await conn.fetch(query, user_uuid, school_id)
        return [self._to_class_dto(record) for record in records]

    async def create_class(self, school_id: int, name: str, class_num: int) -> int:
        query = """INSERT INTO "classes" (school_id, name, class_num) VALUES ($1, $2, $3) RETURNING id"""
        async with get_pool().acquire() as conn:  # type: Connection
            record = await conn.fetchrow(query, school_id, name, class_num)
            return record.get("id")

    async def delete_class(self, class_id: int):
        query = """DELETE FROM "classes" WHERE id=$1"""
        async with get_pool().acquire() as conn:  # type: Connection
            await conn.execute(query, class_id)


