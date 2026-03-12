from dataclasses import dataclass

from asyncpg import Connection

from src.database.dbmanager import get_pool
from src.models.user.user_types import UserBaseType, TeacherType, StudentType


@dataclass
class TeacherWithUser:
    user: UserBaseType
    teacher: TeacherType


@dataclass
class StudentWithUser:
    user: UserBaseType
    student: StudentType


class SchoolMembershipRepository:
    async def get_users(self, school_id: int, start: int = 0, count: int = 10,
                        conn: Connection | None = None) -> list[UserBaseType]:
        pass

    async def get_teachers(self, school_id: int, start: int = 0, count: int = 10,
                           conn: Connection | None = None) -> list[TeacherWithUser]:
        pass

    async def get_students(self, school_id: int, start: int = 0, count: int = 10,
                           conn: Connection | None = None) -> list[StudentWithUser]:
        pass


class SchoolMembershipRepositoryPG(SchoolMembershipRepository):

    def _to_user_obj(self, record) -> UserBaseType:
        return UserBaseType(
            uuid=record["uuid"],
            firstname=record["firstname"],
            surname=record["surname"],
            thirdname=record["thirdname"],
            nickname=record["nickname"],
            type=record["type"])

    def _map_user_obj(self, records) -> list[UserBaseType]:
        return [self._to_user_obj(r)
                for r in records]

    async def get_users(self, school_id: int, start: int = 0, count: int = 10,
                        conn: Connection | None = None) -> list[UserBaseType]:
        if conn:
            return await self._get_users(school_id, conn, start=start, count=count)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._get_users(school_id, conn, start=start, count=count)

    async def _get_users(self, school_id: int, conn: Connection,
                         start: int = 0, count: int = 10) -> list[UserBaseType]:
        query = """
        SELECT 
            us.uuid, us.firstname, 
            us.surname, us.thirdname, 
            us.nickname, us.type
        FROM users_schools_ref AS usr
        JOIN users AS us ON usr.user_uuid = us.uuid
        WHERE usr.school_id = $1
        LIMIT $2 OFFSET $3
        """

        records = await conn.fetch(query, school_id, count, start)
        return self._map_user_obj(records)

    async def get_students(self, school_id: int, start: int = 0,
                           count: int = 10, conn: Connection | None = None) -> list[StudentWithUser]:
        if conn:
            return await self._get_students(school_id, conn, start=start, count=count)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._get_students(school_id, conn, start=start, count=count)

    async def _get_students(self, school_id: int, conn: Connection,
                            start: int = 0, count: int = 10) -> list[StudentWithUser]:
        query = """
        SELECT 
            us.uuid,
            us.firstname,
            us.surname,
            us.thirdname,
            us.nickname,
            us.type,
            st.user_uuid, st.class_id, st.class_num
        FROM users_schools_ref AS usr
        JOIN users us ON usr.user_uuid = us.uuid
        JOIN student_type AS st ON usr.user_uuid = st.user_uuid
        WHERE usr.school_id = $1
        LIMIT $2 OFFSET $3
        """

        records = await conn.fetch(query, school_id, count, start)

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

    async def get_teachers(self, school_id: int, start: int = 0, count: int = 10,
                           conn: Connection | None = None) -> list[TeacherWithUser]:
        if conn:
            return await self._get_teachers(school_id, conn, start=start, count=count)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._get_teachers(school_id, conn, start=start, count=count)

    async def _get_teachers(self, school_id: int, conn: Connection,
                            start: int = 0, count: int = 10) -> list[TeacherWithUser]:
        query = """
        SELECT
            us.uuid,
            us.firstname,
            us.surname,
            us.thirdname,
            us.nickname,
            us.type,
            tch.user_uuid,
            tch.id,
            tch.subject_id
        FROM users_schools_ref usr
        JOIN users us ON usr.user_uuid = us.uuid
        JOIN teacher_type tch ON usr.user_uuid = tch.user_uuid
        WHERE usr.school_id = $1
        LIMIT $2 OFFSET $3
        """

        records = await conn.fetch(query, school_id, count, start)

        return [
            TeacherWithUser(
                self._to_user_obj(r),
                TeacherType(
                    id=r["id"],
                    user_uuid=r["user_uuid"],
                    subject_id=r["subject_id"])
            )
            for r in records
        ]
