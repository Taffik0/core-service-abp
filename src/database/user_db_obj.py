from src.database import dbmanager

from src.models.users import UserBase
from src.models.user import user_fabric

from src.utils import user_sql_generator


async def insert_user(user: UserBase):
    queries = user_sql_generator.build_tables_insert_sql(user.get_tables())  # generate sql
    async with dbmanager.db_pool.acquire() as conn:
        for sql, params in queries:
            await conn.execute(sql, *params)


async def get_user_data(uuid) -> UserBase | None:
    async with dbmanager.db_pool.acquire() as conn:
        user_dict = await conn.fetchrow(f"""SELECT
                                        u.uuid,
                                        u.nickname,
                                        u.firstname,
                                        u.surname,
                                        u.thirdname,
                                        u.type,
                                        s.school_id,
                                        st.class_num,
                                        st.class_id
                                    FROM users u
                                    LEFT JOIN school_ref s ON s.user_uuid = u.uuid
                                    LEFT JOIN student_type st ON st.user_uuid = u.uuid
                                    WHERE u.uuid = $1;""", uuid)
        if not user_dict:
            return None
        return user_fabric.create_user_by_dict(user_dict)


async def delete_user_by_uuid(uuid: str):
    tables = [
        "student_type",
        "teacher_type",
        "admin_type",
        "principal_type",
        "school_ref",
        "user"
    ]

    async with dbmanager.db_pool.acquire() as conn:
        # удаляем сначала дочерние таблицы, потом user
        for table in tables:
            sql = f"DELETE FROM {table} WHERE uuid = $1;"
            await conn.execute(sql, uuid)


async def update_user(user: UserBase):
    tables = user.get_tables()
    async with dbmanager.db_pool.acquire() as conn:
        index = 1
        for table, data in tables.items():
            fields = list(data.keys())
            set_clause = ", ".join(f"{f} = ${i+1}" for i, f in enumerate(fields))
            sql = f"UPDATE {table} SET {set_clause} WHERE uuid = ${len(fields)+1};"
            params = list(data.values()) + [user.uuid]
            await conn.execute(sql, *params)
