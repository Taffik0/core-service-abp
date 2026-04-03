from dataclasses import dataclass
from abc import ABC, abstractmethod

from asyncpg import Connection

from src.models.user.user_types import UserBaseType, StudentType, TeacherType
from src.models.user.user_type_enum import UserTypes


@dataclass
class TeacherWithUser:
    user: UserBaseType
    teacher: TeacherType


@dataclass
class StudentWithUser:
    user: UserBaseType
    student: StudentType


class ClassMembershipRepository(ABC):
    """Репозиторий для получения участников класса с их данными"""
    @abstractmethod
    async def get_teachers(self, class_id: int) -> list[TeacherWithUser]:
        pass

    @abstractmethod
    async def get_students(self, class_id: int) -> list[StudentWithUser]:
        pass

    @abstractmethod
    async def get_members(self, class_id) -> list[UserBaseType]:
        pass


class ClassMembershipRepositoryPg(ClassMembershipRepository):
    def __init__(self, conn: Connection):
        self.conn = conn

    def _to_user_obj(self, record) -> UserBaseType:
        return UserBaseType(
            uuid=record["uuid"],
            firstname=record["firstname"],
            surname=record["surname"],
            thirdname=record["thirdname"],
            nickname=record["nickname"],
            type=record["type"])

    async def get_members(self, class_id) -> list[UserBaseType]:
        query = """
            SELECT 
                u.uuid, u.firstname, 
                u.surname, u.thirdname, 
                u.nickname, u.type
            FROM users_classes_ref AS ucr
            JOIN users AS u ON ucr.user_uuid = u.uuid
            WHERE ucr.class_id = $1
        """
        records = await self.conn.fetch(query, class_id)
        return [self._to_user_obj(record) for record in records]

    async def get_teachers(self, class_id: int) -> list[TeacherWithUser]:
        query = """
            SELECT 
                u.uuid, u.firstname, 
                u.surname, u.thirdname, 
                u.nickname, u.type,
                tch.user_uuid,
                tch.id,
                tch.subject_id
            FROM users_classes_ref AS ucr
            JOIN users AS u ON ucr.user_uuid = u.uuid
            JOIN teacher_type tch ON ucr.user_uuid = tch.user_uuid
            WHERE ucr.class_id = $1
            AND u.type = $2
        """
        records = await self.conn.fetch(query, class_id, UserTypes.TEACHER.value)
        return [
            TeacherWithUser(
                self._to_user_obj(r),
                TeacherType(
                    user_uuid=r["user_uuid"],
                    subject_id=r["subject_id"])
            )
            for r in records
        ]

    async def get_students(self, class_id: int) -> list[StudentWithUser]:
        query = """
            SELECT 
                u.uuid, u.firstname, 
                u.surname, u.thirdname, 
                u.nickname, u.type,
                st.user_uuid, st.class_id, st.class_num
            FROM users_classes_ref AS ucr
            JOIN users AS u ON ucr.user_uuid = u.uuid
            JOIN student_type AS st ON ucr.user_uuid = st.user_uuid
            WHERE ucr.class_id = $1
            AND u.type = $2
        """
        records = await self.conn.fetch(query, class_id, UserTypes.STUDENT.value)
        return [
            StudentWithUser(
                self._to_user_obj(r),
                StudentType(
                    class_id=r["class_id"],
                    class_num=r["class_num"],
                    user_uuid=r["user_uuid"])
            )
            for r in records
        ]
