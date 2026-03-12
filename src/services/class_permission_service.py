from uuid import UUID

from src.database.repository.users_schools_ref_repository import UsersSchoolsRefRepository
from src.models.user.user_type_enum import UserTypes

from src.database.repository.users_classes_ref_repository import UsersClassesRefRepository

from src.models.class_policy import ClassScope, PermissionAction, POLICIES


class ClassPermissionService:
    def __init__(self, users_classes_res_repo: UsersClassesRefRepository,
                 users_schools_ref_repository: UsersSchoolsRefRepository):
        self.users_classes_res_repo = users_classes_res_repo
        self.users_schools_ref_repository = users_schools_ref_repository

    async def can(self, uuid: UUID,
                  role: UserTypes,
                  class_id: int,
                  scope: ClassScope,
                  action: PermissionAction) -> bool:

        policy = POLICIES.get((scope, action))
        if not policy:
            return False

        if role not in policy.roles:
            return False

        if not await self.users_classes_res_repo.get_ref(user_uuid=uuid, class_id=class_id):
            return False

        if policy.condition:
            return await getattr(self, policy.condition)(uuid, class_id)

        return True

    async def can_to_student(self, uuid: UUID, user_role: UserTypes, student_uuid: UUID) -> bool:
        if user_role == UserTypes.TEACHER:
            joined = await self.users_classes_res_repo.get_joint_class(uuid, student_uuid)
            return bool(joined)
