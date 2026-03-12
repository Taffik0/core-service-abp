import asyncio
from datetime import datetime, timedelta

from src.database.unit_of_work import UoW

from src.database.repository.outbox_repository import OutBoxRepository

from src.dependencies.outbox_dependensy import build_outbox_repository
from src.logger import logger


class OutBoxCleanDaemon:
    def __init__(self):
        self.out_box_repo: OutBoxRepository | None = None

    async def process(self):
        logger.info("out box cleaner process")
        while True:
            logger.info("clean out box")
            async with UoW() as uow:
                self.out_box_repo = build_outbox_repository(await uow.get_conn())
                await self._process()
            await asyncio.sleep(600)

    async def _process(self):
        await self.out_box_repo.clean_out_box(datetime.now()-timedelta(hours=1))
