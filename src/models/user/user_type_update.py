from dataclasses import dataclass

from pydantic import BaseModel
from typing import List, Optional

from uuid import UUID


@dataclass
class UserBaseTypeUpdate:
    nickname: str | None = None
    firstname: str | None = None
    surname: str | None = None
    thirdname: str | None = None
    type: str | None = None


@dataclass
class TeacherTypeUpdate:
    subject_id: int | None = None


@dataclass
class StudentTypeUpdate:
    class_num: int | None = None
    class_id: int | None = None


@dataclass
class DirectorTypeUpdate:
    pass