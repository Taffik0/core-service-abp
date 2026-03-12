from uuid import UUID

from src.database.repository.school_entry_requests_repository import SchoolEntryRequestRepository
from src.database.repository.school_repository import SchoolRepository

from src.logger import logger


class SendSchoolEntryRequestUseCase:
    def __init__(self, school_entry_requests_repository: SchoolEntryRequestRepository,
                 school_repository: SchoolRepository):
        self.school_entry_requests_repository = school_entry_requests_repository
        self.school_repository = school_repository

    async def send_school_request(self, school_ref: str, user_uuid: UUID) -> bool:
        school = await self.school_repository.get_school_by_ref(school_ref)
        if not school:
            logger.info(f"failed to send entry-request by {user_uuid} with code {school_ref};"
                        f" code No school has the code")
            return False
        request_id = await self.school_entry_requests_repository.create_request(user_uuid, school.id)
        if request_id is not None:
            logger.info(f"send entry-request by {user_uuid} with code {school_ref} "
                        f"for school {school.id} with id {request_id}")
            return True
        logger.info(f"failed to send entry-request by {user_uuid} with code {school_ref};")
        return False
