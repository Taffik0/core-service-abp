from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.database.repository.processed_broker_messages_repository import (ProcessedBrokerMessageRepository,
                                                                          BrokerMessageDBDTO)
from src.database.unit_of_work import UoW
from src.models.broker_events.broker_event_types import BrokerEventType


@dataclass
class BrokerMessageMark:
    event_id: UUID
    event_type: BrokerEventType
    sent_at: datetime


class ProcessedBrokerMessageService:
    def __init__(self, uow: UoW, processed_broker_messages_repo: ProcessedBrokerMessageRepository):
        self.processed_broker_messages_repo = processed_broker_messages_repo
        self.uow = uow

    def _to_message_mark(self, broker_message: BrokerMessageDBDTO) -> BrokerMessageMark:
        return BrokerMessageMark(event_id=broker_message.event_id,
                                 event_type=broker_message.event_type,
                                 sent_at=broker_message.created_at)

    async def fing_marker(self, event_id: UUID, event_type: BrokerEventType) -> BrokerMessageMark | None:
        broker_message = await self.processed_broker_messages_repo.find_message(event_id=event_id,
                                                                                event_type=event_type)
        if broker_message is None:
            return None
        return self._to_message_mark(broker_message)

    async def exists_marker(self, event_id: UUID, event_type: BrokerEventType) -> bool:
        broker_message = await self.processed_broker_messages_repo.find_message(event_id=event_id,
                                                                                event_type=event_type)
        return broker_message is not None

    async def mark_as_processed(self, event_id: UUID, event_type: BrokerEventType) -> bool:
        status = await self.processed_broker_messages_repo.mark_as_processed(event_id, event_type)
        return status

    async def clear_marker_before(self, send_before: datetime) -> int:
        return await self.processed_broker_messages_repo.delete_created_before(send_before)
