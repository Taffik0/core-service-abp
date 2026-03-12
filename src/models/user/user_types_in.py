from pydantic import BaseModel
from typing import List, Optional

from src.models.user.user_type_enum import UserTypes

from uuid import UUID


class UserTypeIn(BaseModel):
    class Config:
        extra = "ignore"


class UserBaseTypeIn(UserTypeIn):
    uuid: UUID
    nickname: str
    firstname: str
    surname: str
    thirdname: str
    type: str


class StudentTypeIn(UserTypeIn):
    uuid: UUID
    class_num: Optional[int] = None
    class_id: Optional[int] = None


class TeacherTypeIn(UserTypeIn):
    uuid: UUID
    subject_id: Optional[int] = None


class DirectorTypeIn(UserTypeIn):
    uuid: UUID


class AdminTypeIn(UserTypeIn):
    uuid: UUID
    privileges: List[str]


class UserIn:
    def __init__(self, user_base: UserBaseTypeIn, users_types: list[UserTypeIn]):
        self.user_base = user_base
        self.users_types = users_types


USER_IN_TYPE_MAP = {
    UserTypes.USER: UserBaseTypeIn,
    UserTypes.STUDENT: StudentTypeIn,
    UserTypes.TEACHER: TeacherTypeIn,
    UserTypes.DIRECTOR: DirectorTypeIn,
    UserTypes.ADMIN: AdminTypeIn,
}