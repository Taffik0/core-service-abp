from src.conf.db_conf import USER, DB_URL, PASSWORD, DATABASE
import asyncpg
from asyncpg import Pool, Connection
from contextlib import asynccontextmanager

from src.logger import logger


db_pool: Pool = None


async def load():
    global db_pool
    db_pool = await asyncpg.create_pool(
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        host=DB_URL,
        port=5432,
        min_size=1,
        max_size=20,
    )
    print(db_pool)


async def close():
    await db_pool.close()


def get_pool() -> Pool:
    if not db_pool:
        logger.error(
            "dbmanager not loaded db_pool is None. Use -> await load() <- to load db")
        raise Exception()
    return db_pool


async def get_conn() -> Connection:
    async with get_pool().acquire() as conn:
        yield conn
