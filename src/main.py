import asyncio

from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from src import kafka_producer
from src.database import dbmanager
from src.routers.routers_init import routers

from src.kafka_listeners import kafka_listaners_init
from src.background_tasks.tasks_init import start_background_processes, stop_background_processes
from src.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    await dbmanager.load()
    kafka_init_task = asyncio.create_task(kafka_listaners_init.init())
    kafka_producer_task = asyncio.create_task(kafka_producer.start())
    await start_background_processes()
    logger.info("started")
    yield

    logger.info("stop")
    await stop_background_processes()

    kafka_init_task.cancel()

    try:
        await kafka_init_task
    except asyncio.CancelledError:
        pass

    try:
        await kafka_listaners_init.stop()
    except Exception as e:
        logger.error(f"Failed to stop kafka listeners: {e}")

    kafka_producer_task.cancel()

    try:
        await kafka_producer_task
    except asyncio.CancelledError:
        pass

    await kafka_producer.stop()
    await dbmanager.close()


origins = [
    "http://localhost",
    "http://127.0.0.1:5678",
    "http://localhost:5678",
    "http://127.0.0.1:80",
    "http://localhost:80",
    "http://5.129.222.142:6010",
    "https://localhost",
    "https://127.0.0.1:5678",
    "https://localhost:5678",
    "https://127.0.0.1:80",
    "https://localhost:80",
    "https://5.129.222.142:6010"
]

app = FastAPI(lifespan=lifespan, root_path="/api/user-data")
app.include_router(routers)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # кто может делать запросы
    allow_credentials=True,     # можно передавать куки
    allow_methods=["*"],        # разрешенные методы: GET, POST...
    allow_headers=["*"],        # разрешенные заголовки
)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0",
                port=5010, log_level="debug", reload=True)
