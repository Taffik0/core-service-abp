from uuid import UUID

from src.database.repository.users_schools_ref_repository import UsersSchoolsRefRepository
from src.models.user.user_type_enum import UserTypes

from src.models.school_policy import SchoolScope, POLICIES, PermissionAction


class SchoolPermissionService:
    def __init__(self, users_schools_ref_repository: UsersSchoolsRefRepository):
        self.users_schools_ref_repository = users_schools_ref_repository

    async def _has_school_public_access(self, user_uuid: UUID, user_role: str, school_id: int)-> bool:
        if UserTypes(user_role) in [UserTypes.DIRECTOR, UserTypes.STUDENT, UserTypes.TEACHER]:
            user_school_ref = await self.users_schools_ref_repository.get_user_school_ref(user_uuid, school_id)
            return bool(user_school_ref)
        if user_role == UserTypes.ADMIN:
            return True

    async def _has_school_internal_access(self, user_uuid: UUID, user_role: str, school_id: int) -> bool:
        if user_role == UserTypes.DIRECTOR:
            user_school_ref = await self.users_schools_ref_repository.get_user_school_ref(user_uuid, school_id)
            return bool(user_school_ref)
        if user_role == UserTypes.ADMIN:
            return True

    async def _has_school_manage_access(self, user_uuid: UUID, user_role: str, school_id: int) -> bool:
        if user_role == UserTypes.DIRECTOR:
            user_school_ref = await self.users_schools_ref_repository.get_user_school_ref(user_uuid, school_id)
            return bool(user_school_ref)

    async def can(
        self,
        user_uuid: UUID,
        role: UserTypes,
        school_id: int,
        scope: SchoolScope,
        action: PermissionAction,
    ) -> bool:
        if role == UserTypes.ADMIN:
            return True

        policy = POLICIES.get((scope, action))
        if not policy:
            return False

        if role not in policy.roles:
            return False

        if not await self.users_schools_ref_repository.get_user_school_ref(user_uuid, school_id):
            return False

        if policy.condition:
            return await getattr(self, policy.condition)(user_uuid, school_id)

        return True