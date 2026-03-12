import uuid
from PIL import Image
import io

from src.database import dbmanager


async def add_avatar(user_uuid, avatar):
    avatar_uuid = uuid.uuid4()

    contents = await avatar.read()

    # Открываем через PIL
    image = Image.open(io.BytesIO(contents))

    # Можно конвертировать в JPG для экономии места
    image = image.convert("RGB")

    # Пример сохранения на диск
    save_path = f"media/avatars/{avatar_uuid}.jpg"
    image.save(save_path, format="JPEG", quality=85)

    async with dbmanager.db_pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO avatars (user_uuid, avatar_uuid)
            VALUES ($1, $2)
            ON CONFLICT (user_id) 
            DO UPDATE SET avatar_url = EXCLUDED.avatar_url
        """, user_uuid, avatar_uuid)
