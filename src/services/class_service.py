from uuid import UUID

from src.database.repository.class_repository import ClassRepository
from src.services.school_permission_service import SchoolPermissionService

from src.models.school_policy import SchoolScope, PermissionAction
from src.models.user.user_type_enum import UserTypes
from src.models.classes import ClassPublicDTO, ClassDBDTO


class ClassService:
    def __init__(
            self,
            class_repository: ClassRepository,
            school_permission_service: SchoolPermissionService
    ):
        self.class_repository = class_repository
        self.school_permission_service = school_permission_service

    def _class_db_ro_public(self, class_data: ClassDBDTO):
        return ClassPublicDTO(id=class_data.id,
                              school_id=class_data.school_id,
                              class_num=class_data.class_num,
                              name=class_data.name)

    async def _can_read_classes_of_school(self, school_id: int, user_uuid: UUID, user_role: str):
        return await self.school_permission_service.can(user_uuid, UserTypes(user_role), school_id,
                                                        SchoolScope.CLASSES, PermissionAction.READ)

    async def _can_create_class(self, school_id: int, user_uuid: UUID, user_role: str):
        return await self.school_permission_service.can(user_uuid, UserTypes(user_role), school_id,
                                                        SchoolScope.CLASSES, PermissionAction.WRITE)

    async def _can_delete_class(self, school_id: int, user_uuid: UUID, user_role: str):
        return await self.school_permission_service.can(user_uuid, UserTypes(user_role), school_id,
                                                        SchoolScope.CLASSES, PermissionAction.WRITE)

    async def get_classes(self, school_id: int, user_uuid: UUID, user_role: str) -> list[ClassPublicDTO]:
        if await self._can_read_classes_of_school(school_id, user_uuid, user_role):
            classes = await self.class_repository.get_classes_of_school(school_id)
            return [self._class_db_ro_public(class_data) for class_data in classes]
        return []

    async def get_class(self, class_id: int, user_uuid: UUID, user_role: str) -> ClassDBDTO:
        class_data = await self.class_repository.get_class_by_id(class_id)
        return class_data

    async def get_classes_of_user(self, user_uuid: UUID) -> list[ClassPublicDTO]:
        classes = await self.class_repository.get_classes_of_user(user_uuid)
        return [self._class_db_ro_public(class_data) for class_data in classes]

    async def get_classes_of_user_and_school(self, user_uuid: UUID, school_id: int) -> list[ClassPublicDTO]:
        classes = await self.class_repository.get_classes_of_user_and_school(user_uuid, school_id)
        return [self._class_db_ro_public(class_data) for class_data in classes]

    async def create_class(self, user_uuid: UUID, user_role: str, school_id: int, name: str, class_num: int):
        if await self._can_create_class(school_id, user_uuid, user_role):
            class_id = await self.class_repository.create_class(school_id=school_id, name=name, class_num=class_num)
            return class_id

    async def delete_class(self, class_id: int, user_uuid: UUID, user_role: str):
        class_data = await self.class_repository.get_class_by_id(class_id)
        if await self._can_delete_class(class_data.school_id, user_uuid, user_role):
            await self.class_repository.delete_class(class_id)

