from dataclasses import dataclass

from typing import List, Optional

from src.models.user.user_type_enum import UserTypes

from uuid import UUID

@dataclass
class UserType:
    pass

@dataclass
class UserBaseType(UserType):
    uuid: UUID
    nickname: str
    firstname: str
    surname: str
    thirdname: str
    type: str


@dataclass
class StudentType(UserType):
    user_uuid: UUID
    class_num: Optional[int] = None
    class_id: Optional[int] = None


@dataclass
class TeacherType(UserType):
    user_uuid: UUID
    subject_id: Optional[int] = None


@dataclass
class DirectorType(UserType):
    user_uuid: UUID


@dataclass
class AdminType(UserType):
    user_uuid: UUID
    privileges: List[str]


class User:
    def __init__(self, user_base: UserBaseType, users_types: list[UserType]):
        self.user_base = user_base
        self.users_types = users_types


USER_TYPE_MAP = {
    UserTypes.USER: UserBaseType,
    UserTypes.STUDENT: StudentType,
    UserTypes.TEACHER: TeacherType,
    UserTypes.DIRECTOR: DirectorType,
    UserTypes.ADMIN: AdminType,
}