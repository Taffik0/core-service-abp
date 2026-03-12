from src.database import user_db

USER_DATA_NAME_LIST = ["firstname", "surname", "thirdname", "nickname"]


async def get_main_data(uuid, data_name):
    if not data_name:
        return await user_db.get_user_data(uuid, data_name)
    else:
        data_names = [name.strip() for name in data_name.split(",") if name.strip()]
        invalid = [n for n in data_names if n not in USER_DATA_NAME_LIST]
        if invalid:
            data_names = None
        return await user_db.get_user_data(uuid, data_names)
