from uuid import UUID
from fastapi import APIRouter, Depends
from src.models.users import Student, Teacher, UserBase

from src.dependencies.dependencies import get_teacher_repository

from src.database.repository.teacher_repository import TeacherRepository

from src.database.user_db_obj import get_user_data


router = APIRouter()


@router.get("/teacher-permission")
async def teacher_permission(teacher_uuid: UUID, student_uuid: UUID, subject_id: int,
                             teacher_repository: TeacherRepository = Depends(get_teacher_repository)):
    print(teacher_uuid)
    teacher: Teacher | UserBase = await get_user_data(teacher_uuid)
    student = await get_user_data(student_uuid)
    if not teacher or not student:
        return {"allow": False}
    if teacher.type != "teacher":
        return {"allow": False}
    teacher_classes = teacher_repository.get_teacher_classes_id(teacher_uuid)
    if isinstance(student, Student):
        if (student.class_id in teacher_classes
                and teacher.subject_id == subject_id):
            return {"allow": True}
    return {"allow": False}

