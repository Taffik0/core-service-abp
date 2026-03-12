from fastapi import Depends

from src.database.repository.teacher_repository import TeacherRepository, TeacherRepositoryPG
from src.database.repository.student_repository import StudentRepository, StudentRepositoryPG
from src.database.repository.director_repository import DirectorRepository, DirectorRepositoryPG
from src.database.repository.user_repository import UserRepository, UserRepositoryPG

from src.database.repository.users_schools_ref_repository import UsersSchoolsRefRepositoryPG, UsersSchoolsRefRepository

from src.services.use_case.create_user_use_case import CreateUserUseCase
from src.services.users_service import UsersService
from src.services.student_service import StudentService
from src.services.teacher_service import TeacherService


def ger_user_repository() -> UserRepository:
    return UserRepositoryPG()


def get_teacher_repository() -> TeacherRepository:
    return TeacherRepositoryPG()


def get_student_repository() -> StudentRepository:
    return StudentRepositoryPG()


def get_director_repository() -> DirectorRepository:
    return DirectorRepositoryPG()


def get_users_schools_ref_repository() -> UsersSchoolsRefRepository:
    return UsersSchoolsRefRepositoryPG()


def get_create_user_use_case(
    director_repository: DirectorRepository = Depends(get_director_repository),
    user_repository: UserRepository = Depends(ger_user_repository),
    student_repository: StudentRepository = Depends(get_student_repository),
    teacher_repository: TeacherRepository = Depends(get_teacher_repository),
) -> CreateUserUseCase:
    return CreateUserUseCase(
        director_repository=director_repository,
        user_repository=user_repository,
        student_repository=student_repository,
        teacher_repository=teacher_repository,
    )


def build_create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase(
        director_repository=get_director_repository(),
        user_repository=ger_user_repository(),
        student_repository=get_student_repository(),
        teacher_repository=get_teacher_repository())


def get_teacher_service(
    user_repository: UserRepository = Depends(ger_user_repository),
    teacher_repository: TeacherRepository = Depends(get_teacher_repository),
) -> TeacherService:
    return TeacherService(teacher_repository=teacher_repository,
                          user_repository=user_repository)


def get_student_service(
    user_repository: UserRepository = Depends(ger_user_repository),
    student_repository: StudentRepository = Depends(get_student_repository),
) -> StudentService:
    return StudentService(user_repository=user_repository,
                          student_repository=student_repository)


def get_user_service(user_repository: UserRepository = Depends(ger_user_repository)) -> UsersService:
    return UsersService(user_repository=user_repository)
