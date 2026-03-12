from dataclasses import dataclass
from datetime import datetime

from asyncpg import Connection
from uuid import UUID

from src.models.broker_events.broker_event_types import BrokerEventType


@dataclass
class BrokerMessageDBDTO:
    event_id: UUID
    event_type: BrokerEventType
    created_at: datetime


class ProcessedBrokerMessageRepository:
    async def find_message(self, event_id: UUID, event_type: BrokerEventType) -> BrokerMessageDBDTO | None:
        pass

    async def delete_created_before(self, created_before: datetime) -> int:
        pass

    async def mark_as_processed(self, event_id: UUID, event_type: BrokerEventType) -> bool:
        pass


class ProcessedBrokerMessageRepositoryPg(ProcessedBrokerMessageRepository):
    def __init__(self, conn: Connection):
        self.conn = conn

    def _to_message_dto(self, message):
        return BrokerMessageDBDTO(event_id=message["event_id"],
                                  event_type=BrokerEventType(message["event_type"]),
                                  created_at=message["created_at"])

    async def find_message(self, event_id: UUID, event_type: BrokerEventType) -> BrokerMessageDBDTO | None:
        query = """
        SELECT event_id, event_type, created_at 
        FROM processed_broker_messages 
        WHERE event_id = $1 AND event_type = $2"""
        record = await self.conn.fetchrow(query, event_id, event_type.value)
        if not record:
            return None
        return self._to_message_dto(record)

    async def delete_created_before(self, created_before: datetime) -> int:
        query = """DELETE FROM processed_broker_messages WHERE created_at <= $1"""
        result = await self.conn.execute(query, created_before)
        return int(result.split()[1])

    async def mark_as_processed(self, event_id: UUID, event_type: BrokerEventType) -> bool:
        query = """
        INSERT INTO processed_broker_messages (event_id, event_type) VALUES ($1, $2) ON CONFLICT DO NOTHING"""
        result = await self.conn.execute(query, event_id, event_type.value)
        return int(result.split()[2]) > 0

