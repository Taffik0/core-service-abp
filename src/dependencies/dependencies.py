from fastapi import Depends

from src.services.class_ref_service import ClassRefService
from src.database.repository.class_repository import ClassRepository, ClassRepositoryPG
from src.database.repository.teacher_repository import TeacherRepository, TeacherRepositoryPG


def get_class_ref_service() -> ClassRefService:
    return ClassRefService()


def get_class_repository() -> ClassRepository:
    return ClassRepositoryPG()


def get_teacher_repository() -> TeacherRepository:
    return  TeacherRepositoryPG()