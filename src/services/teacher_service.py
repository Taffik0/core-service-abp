from uuid import UUID

from src.database.repository.user_repository import UserRepository
from src.database.repository.teacher_repository import TeacherRepository

from src.models.service.users import (UserServiceReadDTO,
                                      UserTeacherReadDTO,
                                      TeacherServiceReadDTO)

from src.models.user.user_types import UserBaseType, TeacherType


class TeacherService:
    def __init__(self, user_repository : UserRepository,
                 teacher_repository: TeacherRepository):
        self.teacher_repository = teacher_repository
        self.user_repository = user_repository

    def _to_user_dto(self, user: UserBaseType) -> UserServiceReadDTO:
        return UserServiceReadDTO(
            uuid=user.uuid,
            nickname=user.nickname,
            firstname=user.firstname,
            surname=user.surname,
            thirdname=user.thirdname
        )

    def _to_teacher_dto(self, teach: TeacherType) -> TeacherServiceReadDTO:
        return TeacherServiceReadDTO(subject_id=teach.subject_id)

    async def get_teacher(self, teacher_uuid: UUID) -> UserTeacherReadDTO | None:
        user_db = await self.user_repository.get_user(teacher_uuid)
        teacher_db = await self.teacher_repository.get_teacher(teacher_uuid)
        if not user_db or not teacher_db:
            return None
        return UserTeacherReadDTO(self._to_user_dto(user_db), self._to_teacher_dto(teacher_db))
