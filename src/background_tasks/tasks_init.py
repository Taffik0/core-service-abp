import asyncio

from src.background_tasks.outbox_processor import OutboxProcessorDaemon
from src.background_tasks.outbox_clean import OutBoxCleanDaemon


daemons = [OutboxProcessorDaemon(), OutBoxCleanDaemon()]

tasks = []


async def start_background_processes():
    for daemon in daemons:
        task = asyncio.create_task(daemon.process())
        tasks.append(task)


async def stop_background_processes():
    for tk in tasks:
        tk.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)