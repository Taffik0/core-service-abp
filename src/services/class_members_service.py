from dataclasses import dataclass

from uuid import UUID

from src.database.repository.users_classes_ref_repository import UsersClassesRefRepository, UsersSchoolRefDBDTO
from src.database.repository.class_repository import ClassRepository

from src.services.class_permission_service import ClassPermissionService
from src.models.class_policy import ClassScope, PermissionAction

from src.services.use_case.join_to_class_use_case import JoinToClassUseCase

from src.models.user.user_type_enum import UserTypes


@dataclass
class UserClassRefServiceDTO:
    user_uuid: UUID
    class_id: int


class ClassMemberService:
    def __init__(self,
                 users_classes_ref_repo: UsersClassesRefRepository,
                 class_repo: ClassRepository,
                 class_permission_service: ClassPermissionService,
                 join_to_class_use_case: JoinToClassUseCase):
        self.users_classes_ref_repo = users_classes_ref_repo
        self.class_repo = class_repo
        self.class_permission_service = class_permission_service
        self.join_to_class_use_case = join_to_class_use_case

    def _db_to_service_ref_dto(self, user_ref: UsersSchoolRefDBDTO) -> UserClassRefServiceDTO:
        return UserClassRefServiceDTO(user_uuid=user_ref.user_uuid, class_id=user_ref.class_id)

    async def get_students_of_class(self, user_uuid, user_role: str, class_id: int) -> list[UserClassRefServiceDTO]:
        if not await self.class_permission_service.can(
                user_uuid,
                UserTypes(user_role),
                class_id,
                ClassScope.STUDENTS,
                PermissionAction.READ):
            return []
        students_refs = await self.users_classes_ref_repo.get_refs_of_class_by_role(class_id, UserTypes.STUDENT)
        return [self._db_to_service_ref_dto(ur) for ur in students_refs]

    async def get_teacher_of_class(self, user_uuid, user_role: str, class_id: int) -> list[UserClassRefServiceDTO]:
        if not await self.class_permission_service.can(
                user_uuid,
                UserTypes(user_role),
                class_id,
                ClassScope.TEACHERS,
                PermissionAction.READ):
            return []
        teachers_refs = await self.users_classes_ref_repo.get_refs_of_class_by_role(class_id, UserTypes.TEACHER)
        return [self._db_to_service_ref_dto(ur) for ur in teachers_refs]

    async def appoint_members(self, called_uuid: UUID, called_role: str, member_uuid: UUID, class_id: int):
        if not await self.class_permission_service.can(
                called_uuid,
                UserTypes(called_role),
                class_id,
                ClassScope.MEMBERS,
                PermissionAction.WRITE):
            return
        await self.join_to_class_use_case.join(member_uuid, class_id)

