from src.database import dbmanager

from src.models.classes import ClassModel


async def get_class_by_ref(ref: str) -> ClassModel | None:
    async with dbmanager.db_pool.acquire() as conn:
        class_dict = await conn.fetchrow("""SELECT id ,school_id, class_ref, class_num, name 
                                            FROM classes 
                                            WHERE class_ref = $1""", ref)
        if class_dict:
            return ClassModel(**class_dict)
        else:
            return None
