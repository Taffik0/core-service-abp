from dataclasses import dataclass
from uuid import UUID, uuid4

from src.logger import logger

from src.database.repository.school_repository import SchoolRepository
from src.database.repository.users_schools_ref_repository import UsersSchoolsRefRepository
from src.models.dto.school_db_dto import SchoolDBDTO
from src.models.user.user_type_enum import UserTypes
from src.services.school_permission_service import SchoolPermissionService
from src.models.school_policy import SchoolScope, PermissionAction


@dataclass
class SchoolPublicDTO:
    id: int
    name: str
    description: str


@dataclass
class SchoolAdminDTO(SchoolPublicDTO):
    ref: str | None


class SchoolService:
    def __init__(self, school_repository: SchoolRepository,
                 users_schools_ref_repository: UsersSchoolsRefRepository,
                 school_permission_service: SchoolPermissionService):
        self.school_repository = school_repository
        self.users_schools_ref_repository = users_schools_ref_repository
        self.school_permission_service = school_permission_service

    async def get_schools_of_user(self, user_uuid: UUID, user_role: str, count: int | None = None, start: int = 0
                                  ) -> list[SchoolPublicDTO] | list[SchoolAdminDTO]:
        schools = await self.school_repository.get_school_of_user(user_uuid, count=count, start=start)
        if UserTypes(user_role) in [UserTypes.TEACHER, UserTypes.USER]:
            return [self._to_public_dto(school) for school in schools]
        if UserTypes(user_role) in [UserTypes.DIRECTOR]:
            return [self._to_admin_dto(school) for school in schools]
        return []

    async def get_schools(self, user_uuid: UUID, user_role: str, count: int, start: int = 0
                          ) -> list[SchoolPublicDTO] | list[SchoolAdminDTO]:
        if UserTypes(user_role) == UserTypes.DIRECTOR:
            schools = await self.school_repository.get_schools(count, start)
            return [self._to_public_dto(school) for school in schools]
        return await self.get_schools_of_user(user_uuid, user_role, count=count, start=start)

    async def get_school(self, user_uuid: UUID, user_role: str, school_id: int) -> SchoolPublicDTO:
        if self._has_school_internal_access(user_uuid, user_role, school_id):
            school = await self.school_repository.get_school(school_id)
            return self._to_admin_dto(school)
        if self._has_school_public_access(user_uuid, user_role, school_id):
            school = await self.school_repository.get_school(school_id)
            return self._to_public_dto(school)

    async def create_school(self, user_uuid: UUID, user_role: str,
                            school_name: str, school_description: str) -> int | None:
        logger.info(f"user {user_uuid} {user_role} try create school")
        if UserTypes(user_role) == UserTypes.DIRECTOR:
            logger.info(f"create school for - {user_uuid}")
            sc_id = await self.school_repository.create_school(school_name, school_description)
            if sc_id is None:
                logger.warning(f"school for {user_uuid} not created")
                return None
            logger.info(f"creates school for {user_uuid} create with id - {sc_id}")
            await self.users_schools_ref_repository.create_user_school_ref(user_uuid, sc_id)
            return sc_id

    def _to_public_dto(self, school: SchoolDBDTO) -> SchoolPublicDTO:
        return SchoolPublicDTO(
            id=school.id,
            name=school.name,
            description=school.description,
        )

    def _to_admin_dto(self, school: SchoolDBDTO) -> SchoolPublicDTO:
        return SchoolAdminDTO(
            id=school.id,
            name=school.name,
            description=school.description,
            ref=school.ref
        )

    async def set_school_ref(self, user_uuid: UUID, user_role: str, school_id: int,
                       ref: str | None, auto_get: bool = False):
        if self._has_school_manage_access(user_uuid, user_role, school_id):
            logger.info(f"try to ser ref of school - {school_id} for user - {user_uuid} with role {user_role}")
            if auto_get:
                ref = str(uuid4())
            await self.school_repository.set_ref(school_id, ref)

    async def change_school(self, user_uuid: UUID, user_role: str,
                            school_id: int, name: str | None, description: str | None):
        if self._has_school_manage_access(user_uuid, user_role, school_id):
            await self.school_repository.change_school(school_id=school_id, name=name, description=description)

    async def delete_school(self, user_uuid: UUID, user_role: str, school_id: int):
        if self._has_school_manage_access(user_uuid, user_role, school_id):
            await self.school_repository.delete_school(school_id)

    async def _has_school_public_access(self, user_uuid: UUID, user_role: str, school_id: int) -> bool:
        return await self.school_permission_service.can(
            user_uuid, UserTypes(user_role), school_id,
            SchoolScope.PUBLIC, PermissionAction.READ)

    async def _has_school_internal_access(self, user_uuid: UUID, user_role: str, school_id: int) -> bool:
        return await self.school_permission_service.can(
            user_uuid, UserTypes(user_role), school_id,
            SchoolScope.INTERNAL, PermissionAction.READ)

    async def _has_school_manage_access(self, user_uuid: UUID, user_role: str, school_id: int) -> bool:
        return await self.school_permission_service.can(
            user_uuid, UserTypes(user_role), school_id,
            SchoolScope.INTERNAL, PermissionAction.WRITE)
