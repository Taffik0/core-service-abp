from uuid import UUID

from src.database.repository.user_repository import UserRepository
from src.database.repository.student_repository import StudentRepository

from src.models.service.users import (UserServiceReadDTO,
                                      UserStudentReadDTO,
                                      StudentServiceReadDTO)

from src.models.user.user_types import UserBaseType, StudentType


class StudentService:
    def __init__(self, user_repository: UserRepository,
                 student_repository: StudentRepository):
        self.student_repository = student_repository
        self.user_repository = user_repository

    def _to_user_dto(self, user: UserBaseType) -> UserServiceReadDTO:
        return UserServiceReadDTO(
            uuid=user.uuid,
            nickname=user.nickname,
            firstname=user.firstname,
            surname=user.surname,
            thirdname=user.thirdname
        )

    def _to_student_dto(self, st: StudentType) -> StudentServiceReadDTO:
        return StudentServiceReadDTO(class_num=st.class_num, class_id=st.class_id)

    async def get_student(self, student_uuid: UUID) -> UserStudentReadDTO | None:
        user_db = await self.user_repository.get_user(student_uuid)
        teacher_db = await self.student_repository.get_student(student_uuid)
        if not user_db or not teacher_db:
            return None
        return UserStudentReadDTO(self._to_user_dto(user_db), self._to_student_dto(teacher_db))