from typing import Callable, Type, Awaitable, Dict
from uuid import UUID

from src.database.repository.user_repository import UserRepository
from src.database.repository.teacher_repository import TeacherRepository
from src.database.repository.student_repository import StudentRepository
from src.database.repository.director_repository import DirectorRepository

from src.models.user.user_types import User, TeacherType, StudentType, DirectorType, UserType

from src.logger import logger


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository,
                 student_repository: StudentRepository,
                 teacher_repository: TeacherRepository,
                 director_repository: DirectorRepository):
        self.user_repository = user_repository
        self.student_repository = student_repository
        self.teacher_repository = teacher_repository
        self.director_repository = director_repository

        self.repos_type_mup = {
            TeacherType: self.teacher_repository,
            StudentType: self.student_repository,
        }
        self.repo_func_mup: Dict[
            Type[UserType],
            Callable[[UUID, UserType], Awaitable[None]]
        ] = {
            TeacherType: self.insert_teacher,
            StudentType: self.insert_student,
            DirectorType: self
        }

    async def insert_teacher(self, user_uuid: UUID, user_data: UserType):
        logger.info("create teacher")
        if isinstance(user_data, TeacherType):
            await self.teacher_repository.crate_teacher_type(user_uuid, user_data)

    async def insert_student(self, user_uuid: UUID, user_data: UserType):
        logger.info("create student")
        if isinstance(user_data, StudentType):
            await self.student_repository.create_student(user_uuid, user_data)

    async def insert_director(self, user_uuid, user_data: UserType):
        logger.info("create director")
        if isinstance(user_data, DirectorType):
            await self.director_repository.create_director(user_uuid, user_data)

    async def create_user(self, user: User):
        logger.info("create user")
        await self.user_repository.create_user(user.user_base)

        for user_type in user.users_types:
            func = self.repo_func_mup.get(type(user_type))
            if func:
                await func(user.user_base.uuid, user_type)

