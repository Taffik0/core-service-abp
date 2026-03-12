from dataclasses import dataclass

from uuid import UUID


@dataclass
class SchoolDBDTO:
    id: int
    name: str
    description: str
    ref: str | None


@dataclass
class SchoolEntryRequestsDTO:
    id: int
    user_uuid: UUID
    school_id: int
