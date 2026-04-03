from uuid import UUID

from src.database.repository.users_schools_ref_repository import UsersSchoolsRefRepository
from src.models.user.user_type_enum import UserTypes

from src.database.repository.users_classes_ref_repository import UsersClassesRefRepository
from src.database.repository.class_repository import ClassRepository

from src.models.class_policy import ClassScope, PermissionAction, POLICIES

from src.logger import logger


class ClassPermissionService:
    def __init__(self, users_classes_res_repo: UsersClassesRefRepository,
                 users_schools_ref_repository: UsersSchoolsRefRepository,
                 class_repo: ClassRepository):
        self.users_classes_res_repo = users_classes_res_repo
        self.users_schools_ref_repository = users_schools_ref_repository
        self.class_repo = class_repo

    async def can(self, uuid: UUID,
                  role: UserTypes,
                  class_id: int,
                  scope: ClassScope,
                  action: PermissionAction) -> bool:

        policy = POLICIES.get((scope, action))
        if not policy:
            return False

        if role.DIRECTOR:
            school_class = await self.class_repo.get_class_by_id(class_id)
            school_ref = await self.users_schools_ref_repository.get_user_school_ref(user_uuid=uuid,
                                                                                     school_id=school_class.school_id)
            if school_ref:
                return True

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
