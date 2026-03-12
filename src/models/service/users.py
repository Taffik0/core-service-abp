from dataclasses import dataclass

from uuid import UUID


@dataclass
class UserServiceReadDTO:
    uuid: UUID
    nickname: str
    firstname: str
    surname: str
    thirdname: str


@dataclass
class TeacherServiceReadDTO:
    subject_id: int


@dataclass
class StudentServiceReadDTO:
    class_num: int
    class_id: int


@dataclass
class UserStudentReadDTO:
    user: UserServiceReadDTO
    student: StudentServiceReadDTO


@dataclass
class UserTeacherReadDTO:
    user: UserServiceReadDTO
    teacher: TeacherServiceReadDTO