from dataclasses import dataclass
from datetime import datetime

from uuid import UUID
from asyncpg import Connection

from src.models.broker_events.broker_event_types import BrokerEventType

@dataclass
class EventMessageDBDTO:
    id: int
    event_id: UUID | None
    event_type: BrokerEventType
    payload: dict
    sent: bool
    created_at: datetime


class OutBoxRepository:
    async def get_message(self, sent_time: datetime) -> list[EventMessageDBDTO]:
        pass

    async def create_message(self, event_id: UUID | None, event_type: BrokerEventType, payload: dict) -> int | None:
        pass

    async def set_sent(self, sent: bool, message_id: int) -> bool:
        pass

    async def clean_out_box(self, sent_at: datetime) -> int:
        pass


class OutBoxRepositoryPG(OutBoxRepository):
    def __init__(self, conn: Connection):
        self.conn = conn

    def _to_db_dto(self, message) -> EventMessageDBDTO:
        return EventMessageDBDTO(
            id=message["id"],
            event_id=message["message_id"],
            event_type=BrokerEventType(message["event_type"]),
            payload=message["payload"],
            sent=message["sent"],
            created_at=message["created_at"])

    async def get_message(self, sent_time: datetime) -> list[EventMessageDBDTO]:
        query = """SELECT id, event_id, event_type, payload, sent, created_at FROM outbox WHERE created_at <= $1"""
        records = await self.conn.fetch(query, sent_time)
        return [self._to_db_dto(record) for record in records]

    async def create_message(self, event_id: UUID | None, event_type: BrokerEventType, payload: dict) -> int | None:
        query = """INSERT INTO outbox (event_id, event_type, payload) VALUES ($1, $2, $3) RETURNING id"""
        record = await self.conn.fetchrow(query, event_id, event_type, payload)
        if record is None:
            return None
        return record["id"]

    async def set_sent(self, sent: bool, message_id: int) -> bool:
        query = """UPDATE outbox SET sent=$1 WHERE id=$2"""
        result = await self.conn.execute(query, sent, message_id)
        success = result.startswith("UPDATE") and int(result.split()[1]) > 0
        return success

    async def clean_out_box(self, sent_at: datetime) -> int:
        query = """DELETE FROM outbox WHERE created_at <= $1 AND sent = true"""
        result = await self.conn.execute(query, sent_at)
        return int(result.split()[1])

