import asyncio
from datetime import datetime

from src.database.unit_of_work import UoW
from src.dependencies.outbox_dependensy import build_outbox_repository

from src.database.repository.outbox_repository import OutBoxRepository

from src.kafka_producer import get_producer_json, send_dict

from src.logger import logger


MAX_DELAY = 10
STANDARD_DELAY = 1
delay = STANDARD_DELAY


class OutboxProcessorDaemon:
    def __init__(self):
        self.out_box_repo: OutBoxRepository | None = None

    async def process(self):
        logger.info("out box process")
        while True:
            async with UoW() as uow:
                self.out_box_repo = build_outbox_repository(await uow.get_conn())
                await self._process()
            await asyncio.sleep(delay)

    async def _process(self):
        global delay, MAX_DELAY, STANDARD_DELAY
        messages = await self.out_box_repo.get_message(datetime.now())

        for msg in messages:
            data = msg.payload
            if msg.event_id:
                data["event_id"] = msg.event_id
            try:
                await send_dict(msg)
                await self.out_box_repo.set_sent(True, msg.id)
            except:
                logger.warn("can't use producer")
