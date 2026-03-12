from uuid import UUID

from src.database.repository.school_membership_repository import SchoolMembershipRepository
from src.database.repository.users_schools_ref_repository import UsersSchoolsRefRepository
from src.services.school_permission_service import SchoolPermissionService

from src.models.school_policy import SchoolScope, PermissionAction
from src.models.user.user_type_enum import UserTypes
from src.models.user.user_types import UserBaseType, StudentType, TeacherType

from src.models.service.users import (
    UserServiceReadDTO,
    UserTeacherReadDTO,
    UserStudentReadDTO,
    TeacherServiceReadDTO,
    StudentServiceReadDTO)


class SchoolMemberService:
    def __init__(
            self,
            school_membership_repository: SchoolMembershipRepository,
            school_permission_service: SchoolPermissionService,
            users_schools_ref_repo: UsersSchoolsRefRepository
    ):
        self.school_membership_repository = school_membership_repository
        self.school_permission_service = school_permission_service
        self.users_schools_ref_repo = users_schools_ref_repo

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

    def _to_student_dto(self, st: StudentType) -> StudentServiceReadDTO:
        return StudentServiceReadDTO(class_num=st.class_num, class_id=st.class_id)

    async def get_teachers(self, school_id: int, user_uuid: UUID, user_role: str,
                           count: int = 40, start: int = 0) -> list[UserTeacherReadDTO]:
        can = await self.school_permission_service.can(
            user_uuid,
            UserTypes(user_role),
            school_id,
            SchoolScope.TEACHERS,
            PermissionAction.READ)
        if not can:
            return []

        db_teacher = await self.school_membership_repository.get_teachers(school_id, start=start, count=count)
        return [UserTeacherReadDTO(
            self._to_user_dto(teach.user),
            self._to_teacher_dto(teach.teacher))
            for teach in db_teacher
        ]

    async def get_students(self, school_id: int, user_uuid: UUID, user_role: str,
                           count: int = 40, start: int = 0) -> list[UserStudentReadDTO]:
        can = await self.school_permission_service.can(
            user_uuid,
            UserTypes(user_role),
            school_id,
            SchoolScope.STUDENTS,
            PermissionAction.READ)

        if not can:
            return []

        db_students = await self.school_membership_repository.get_students(school_id, start=start, count=count)
        return [UserStudentReadDTO(
            self._to_user_dto(stud.user),
            self._to_student_dto(stud.student))
            for stud in db_students
        ]

    async def delete_ref(self, called_uuid, called_role: str, user_uuid: UUID, school_id: int):
        can = await self.school_permission_service.can(
            called_uuid,
            UserTypes(called_role),
            school_id,
            SchoolScope.MEMBERS,
            PermissionAction.WRITE)
        if not can:
            return
        await self.users_schools_ref_repo.delete_user_school_ref(user_uuid, school_id)

