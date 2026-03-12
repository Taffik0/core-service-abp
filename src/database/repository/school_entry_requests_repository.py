from uuid import UUID

from asyncpg import Connection, UniqueViolationError

from src.database.dbmanager import get_pool
from src.models.school_entry_requests_models import SchoolEntryRequestsStatus, SchoolEntryRequestsDBDTO


class SchoolEntryRequestRepository:
    async def get_pending_requests(self, school_id: int) -> list[SchoolEntryRequestsDBDTO]:
        pass

    async def get_requests(self, school_id: int, status: SchoolEntryRequestsStatus) -> list[SchoolEntryRequestsDBDTO]:
        pass

    async def get_request(self, request_id: int) -> SchoolEntryRequestsDBDTO | None:
        pass

    async def create_request(self, user_uuid: UUID, school_id: int,
                             conn: Connection | None = None) -> int | None:
        pass

    async def set_status(self, request_id: int, status: SchoolEntryRequestsStatus,
                         conn: Connection | None = None) -> bool:
        pass


class SchoolEntryRequestRepositoryPG(SchoolEntryRequestRepository):

    async def get_requests(self, school_id: int, status: SchoolEntryRequestsStatus) -> list[SchoolEntryRequestsDBDTO]:
        query = """
        SELECT id, user_uuid, school_id, status, created_at, updated_at 
        FROM school_entry_requests
        WHERE school_id = $1 AND status = $2"""
        async with get_pool().acquire() as conn:  # type: Connection
            request_records = await conn.fetch(query, school_id, status.value)
            return [
                SchoolEntryRequestsDBDTO(
                    id=record["id"],
                    school_id=record["school_id"],
                    user_uuid=record["user_uuid"],
                    status=SchoolEntryRequestsStatus(record["status"]),
                    created_at=record["created_at"],
                    updated_at=record["updated_at"]
                )
                for record in request_records
            ]

    async def get_pending_requests(self, school_id: int) -> list[SchoolEntryRequestsDBDTO]:
        return await self.get_requests(school_id=school_id, status=SchoolEntryRequestsStatus.PENDING)

    async def get_request(self, request_id: int) -> SchoolEntryRequestsDBDTO | None:
        query = """
        SELECT id, user_uuid, school_id, status, created_at, updated_at 
        FROM school_entry_requests
        WHERE id = $1"""
        async with get_pool().acquire() as conn:  # type: Connection
            record = await conn.fetchrow(query, request_id)
        if not record:
            return None
        return SchoolEntryRequestsDBDTO(
            id=record["id"],
            school_id=record["school_id"],
            user_uuid=record["user_uuid"],
            status=SchoolEntryRequestsStatus(record["status"]),
            created_at=record["created_at"],
            updated_at=record["updated_at"]
        )

    async def create_request(self, user_uuid: UUID, school_id: int,
                             conn: Connection | None = None) -> int:
        if conn is not None:
            return await self._create_request(user_uuid, school_id, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._create_request(user_uuid, school_id, conn)

    async def _create_request(self, user_uuid: UUID, school_id: int,
                              conn: Connection) -> int | None:
        query = """
        INSERT INTO school_entry_requests (user_uuid, school_id, status)
        VALUES ($1, $2, $3)
        RETURNING id
        """
        try:
            record = await conn.fetchrow(query, user_uuid, school_id, SchoolEntryRequestsStatus.PENDING.value)
        except UniqueViolationError:
            return None
        return record["id"]

    async def set_status(self, request_id: int, status: SchoolEntryRequestsStatus,
                         conn: Connection | None = None) -> bool:
        if conn is not None:
            return await self._set_status(request_id, status, conn)
        async with get_pool().acquire() as conn:  # type: Connection
            return await self._set_status(request_id, status, conn)

    async def _set_status(self, request_id: int, status: SchoolEntryRequestsStatus,
                          conn: Connection) -> bool:
        query = """
        UPDATE school_entry_requests
        SET status = $2
        WHERE id = $1
        """

        result = await conn.execute(query, request_id, status.value)
        return result != "UPDATE 0"
