from src.models.users import UserBase, SchoolRef, Student, Teacher, Admin, Director

from src.logger import logger

from src.utils.user_sql_generator import build_tables_insert_sql


USER_TYPE_MAP = {
    "student": Student,
    "teacher": Teacher,
    "admin": Admin,
    "user": UserBase,
    "director": Director
}


def create_user_by_dict(user: dict) -> UserBase | None:
    if not user:
        return None
    cls = USER_TYPE_MAP.get(user.get("type"))
    if cls is None:
        logger.warning(f"Unknown user type: {user.get('type')}")
    return cls(**user)


def create_dict_by_user(user: UserBase) -> dict:
    return user.dict()


if __name__ == "__main__":
    student_dict = {
        "uuid": "e7a1a2c8-3d4f-4b9c-9f02-12c3f5ba1234",
        "nickname": "taffik",
        "firstname": "Иван",
        "surname": "Иванов",
        "thirdname": "Иванович",
        "type": "student",

        "school_id": 42,
        "class_num": 10,
        "class_ref": "A1",

        # Лишние поля будут проигнорированы, если extra="ignore"
        "something_extra": "will_be_ignored"
    }
    user = create_user_by_dict(student_dict)
    print(user.dict())
    print(user.get_tables())
    print(build_tables_insert_sql(user.get_tables()))
