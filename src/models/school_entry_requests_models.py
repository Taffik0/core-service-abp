from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from uuid import UUID


class SchoolEntryRequestsStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'


@dataclass
class SchoolEntryRequestsDBDTO:
    id: int
    user_uuid: UUID
    school_id: int
    status: SchoolEntryRequestsStatus
    created_at: datetime
    updated_at: datetime