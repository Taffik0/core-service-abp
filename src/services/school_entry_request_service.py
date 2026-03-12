from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.database.dbmanager import get_pool

from src.logger import logger

from src.database.repository.school_entry_requests_repository import SchoolEntryRequestRepository
from src.models.school_entry_requests_models import SchoolEntryRequestsStatus

from src.services.school_permission_service import SchoolPermissionService
from src.services.use_case.join_to_school_use_case import JoinToSchoolUseCase
from src.models.school_policy import SchoolScope, PermissionAction
from src.models.user.user_type_enum import UserTypes
from src.models.school_entry_requests_models import SchoolEntryRequestsDBDTO


@dataclass
class SchoolEntryRequestDTO:
    id: int
    user_uuid: UUID
    school_id: int
    status: SchoolEntryRequestsStatus
    created_at: datetime
    updated_at: datetime


class SchoolEntryRequestService:
    def __init__(
            self,
            school_entry_requests_repository: SchoolEntryRequestRepository,
            school_permission_service: SchoolPermissionService,
            join_to_school_use_case: JoinToSchoolUseCase,
    ):
        self.school_entry_requests_repository = school_entry_requests_repository
        self.school_permission_service = school_permission_service
        self.join_to_school_use_case = join_to_school_use_case

    def _map_to_dto(self, requests_db_dto: list[SchoolEntryRequestsDBDTO]) -> list[SchoolEntryRequestDTO]:
        return [
            self._to_dto(r)
            for r in requests_db_dto
        ]

    def _to_dto(self, request_db_dto: SchoolEntryRequestsDBDTO) -> SchoolEntryRequestDTO:
        return SchoolEntryRequestDTO(
                id=request_db_dto.id,
                user_uuid=request_db_dto.user_uuid,
                school_id=request_db_dto.school_id,
                status=request_db_dto.status,
                created_at=request_db_dto.created_at,
                updated_at=request_db_dto.updated_at,
            )

    async def _check_read_permission(self, school_id: int, user_uuid: UUID, user_role: str) -> bool:
        return await self.school_permission_service.can(
            user_uuid,
            UserTypes(user_role),
            school_id,
            SchoolScope.ENTRY_REQUEST,
            PermissionAction.READ
        )

    async def _check_set_status_permission(self, entry_request: SchoolEntryRequestDTO,
                                           user_uuid: UUID, user_role: str) -> bool:
        school_id = entry_request.school_id
        can = await self.school_permission_service.can(
            user_uuid,
            UserTypes(user_role),
            school_id,
            SchoolScope.ENTRY_REQUEST,
            PermissionAction.WRITE
        )

        return can and entry_request.status == SchoolEntryRequestsStatus.PENDING

    async def get_entry_requests(self, school_id: int, user_uuid: UUID, user_role: str) -> list[SchoolEntryRequestDTO]:
        can = await self._check_read_permission(school_id, user_uuid, user_role)
        if not can:
            return []

        requests_db_dto = await self.school_entry_requests_repository.get_requests(
            school_id,
            SchoolEntryRequestsStatus.PENDING
        )

        return self._map_to_dto(requests_db_dto)

    async def get_entry_request(self, request_id: int, user_uuid: UUID, user_role: str) -> SchoolEntryRequestDTO:
        request_db_dto = await self.school_entry_requests_repository.get_request(request_id)
        request_dto = self._to_dto(request_db_dto)
        can = await self._check_read_permission(request_dto.school_id, user_uuid, user_role)
        if can:
            return request_dto

    async def submit_entry_request(self, request_id: int, user_uuid: UUID, user_role: str):
        async with get_pool().acquire() as conn:
            async with conn.transaction():
                request_db_dto = await self.school_entry_requests_repository.get_request(request_id)
                request_dto = self._to_dto(request_db_dto)
                school_id = request_dto.school_id
                can = await self._check_set_status_permission(request_dto, user_uuid, user_role)
                if not can:
                    logger.info(f"user - {user_uuid} can't submit {request_id}")
                    return
                await self.school_entry_requests_repository.set_status(request_id,
                                                                       SchoolEntryRequestsStatus.APPROVED,
                                                                       conn=conn)
                await self.join_to_school_use_case.join_to_school(request_dto.user_uuid, school_id, conn=conn)

    async def reject_entry_request(self, request_id: int, user_uuid: UUID, user_role: str):
        request_db_dto = await self.school_entry_requests_repository.get_request(request_id)
        request_dto = self._to_dto(request_db_dto)
        can = await self._check_set_status_permission(request_dto, user_uuid, user_role)
        if not can:
            return
        await self.school_entry_requests_repository.set_status(request_id, SchoolEntryRequestsStatus.REJECTED)
