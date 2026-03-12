import asyncio
import asyncpg
from src.database import dbmanager  # предполагается, что у тебя есть объект db_pool


async def add_user(data):
    async with dbmanager.db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (uuid, firstname, surname, thirdname, nickname)
            VALUES ($1, $2, $3, $4, $5)
        """, data["uuid"], data["firstname"], data["surname"], data["thirdname"], data["nickname"])


async def get_user_data(uuid, data_names=None):
    select_data = "*"
    if data_names:
        # Используем массив колонок через SQL идентификаторы
        select_data = ', '.join(data_names)

    async with dbmanager.db_pool.acquire() as conn:
        row = await conn.fetchrow(f"SELECT {select_data} FROM users WHERE uuid = $1", uuid)

    if not row:
        return None

    user_data = dict(row)

    if data_names is None:
        user_data.pop("uuid", None)

    return user_data
