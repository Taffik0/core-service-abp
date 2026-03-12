from dataclasses import dataclass

from pydantic import BaseModel


class ClassModel(BaseModel):
    id: int
    school_id: int
    class_ref: str
    class_num: int
    name: str


@dataclass
class ClassDBDTO:
    id: int
    school_id: int
    class_ref: str
    class_num: int
    name: str


@dataclass
class ClassPublicDTO:
    id: int
    school_id: int
    class_num: int
    name: str


@dataclass
class ClassInternalDTO:
    id: int
    school_id: int
    class_ref: str
    class_num: int
    name: str
