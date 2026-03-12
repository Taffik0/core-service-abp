from pydantic import BaseModel
from typing import List, Optional

from uuid import UUID


class UserBase(BaseModel):
    uuid: UUID
    nickname: str
    firstname: str
    surname: str
    thirdname: str
    type: str

    class Config:
        extra = "ignore"

    def own_dict(self, cls_for_fields):
        """
        Ключи берём с cls_for_fields, значения — с self
        """
        class_dict = {k: getattr(self, k) for k in cls_for_fields.__annotations__.keys()}
        return class_dict

    def own_dict_uuid(self, cls_for_fields):
        class_dict = {k: getattr(self, k) for k in cls_for_fields.__annotations__.keys()}
        class_dict["user_uuid"] = self.uuid
        return class_dict

    def get_tables(self):
        return {"users": UserBase.own_dict(self, UserBase)}


class SchoolRef(UserBase):
    school_id: Optional[int] = None

    def get_tables(self):
        return {"school_ref": SchoolRef.own_dict(self, SchoolRef), **super().get_tables()}


class Student(UserBase):
    class_num: Optional[int] = None
    class_id: Optional[int] = None

    def get_tables(self):
        return {"student_type": Student.own_dict_uuid(self, Student), **super().get_tables()}


class Teacher(UserBase):
    subject_id: Optional[int] = None

    def get_tables(self):
        return {"teacher_type": Teacher.own_dict_uuid(self, Teacher), **super().get_tables()}


class Director(UserBase):
    def get_tables(self):
        return {"teacher_type": Teacher.own_dict_uuid(self, Director), **super().get_tables()}


class Admin(UserBase):
    privileges: List[str]

    def get_tables(self):
        return {"admin_type": Admin.own_dict_uuid(self, Admin), **super().get_tables()}

