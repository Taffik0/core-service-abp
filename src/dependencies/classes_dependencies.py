from fastapi import Depends

from src.database.dbmanager import get_conn

from src.dependencies.school_dependencies import get_school_permission_service, get_users_schools_ref_repository
from src.dependencies.user_dependecies import get_student_repository

from src.database.repository.class_repository import ClassRepository, ClassRepositoryPG
from src.database.repository.users_classes_ref_repository import UsersClassesRefRepository, UsersClassesRefRepositoryPG
from src.database.repository.class_membership_repository import ClassMembershipRepository, ClassMembershipRepositoryPg

from src.clients.kafka.join_to_class_event_client import JoinToClassEventClient

from src.services.use_case.join_to_class_use_case import JoinToClassUseCase
from src.services.use_case.join_to_class_by_ref_use_case import JoinToClassByRefUseCase

from src.services.school_permission_service import SchoolPermissionService
from src.services.class_permission_service import ClassPermissionService
from src.services.class_service import ClassService
from src.services.class_members_service import ClassMemberService


def get_class_repository() -> ClassRepository:
    return ClassRepositoryPG()


def get_users_classes_res_repository() -> UsersClassesRefRepository:
    return UsersClassesRefRepositoryPG()


def get_join_to_class_event_client() -> JoinToClassEventClient:
    return JoinToClassEventClient()


def get_class_membership_repository(conn = Depends(get_conn)) -> ClassMembershipRepository:
    return ClassMembershipRepositoryPg(conn)


def get_join_to_class_use_case(
    users_classes_res_repo: UsersClassesRefRepository = Depends(get_users_classes_res_repository),
    students_repo=Depends(get_student_repository),
    join_to_class_event_client: JoinToClassEventClient = Depends(get_join_to_class_event_client),
    class_repo: ClassRepository = Depends(get_class_repository)
) -> JoinToClassUseCase:
    return JoinToClassUseCase(users_classes_ref_repo=users_classes_res_repo,
                              student_repo=students_repo,
                              join_to_class_event_client=join_to_class_event_client,
                              class_repo=class_repo)


def get_join_to_class_by_ref_use_case(
    join_to_class_use_case: JoinToClassUseCase = Depends(get_join_to_class_use_case),
    class_repo: ClassRepository = Depends(get_class_repository),
    users_schools_ref_repo=Depends(get_users_schools_ref_repository),
) -> JoinToClassByRefUseCase:
    return JoinToClassByRefUseCase(join_to_class_use_case=join_to_class_use_case,
                                   class_repo=class_repo,
                                   users_schools_ref_repo=users_schools_ref_repo)


def get_class_service(
        class_repo: ClassRepository = Depends(get_class_repository),
        school_permission_service: SchoolPermissionService = Depends(get_school_permission_service)
) -> ClassService:
    return ClassService(class_repository=class_repo, school_permission_service=school_permission_service)


def get_class_permission_service(
    users_classes_res_repo: UsersClassesRefRepository = Depends(get_users_classes_res_repository),
    users_schools_ref_repo=Depends(get_users_schools_ref_repository),
    class_repo: ClassRepository = Depends(get_class_repository)
) -> ClassPermissionService:
    return ClassPermissionService(users_classes_res_repo=users_classes_res_repo,
                                  users_schools_ref_repository=users_schools_ref_repo,
                                  class_repo=class_repo)


def get_class_member_service(
    users_classes_res_repo: UsersClassesRefRepository = Depends(get_users_classes_res_repository),
    class_membership_repo: ClassMembershipRepository = Depends(get_class_membership_repository),
    class_permission_service: ClassPermissionService = Depends(get_class_permission_service),
    join_to_class_uc: JoinToClassUseCase = Depends(get_join_to_class_use_case)
) -> ClassMemberService:
    return ClassMemberService(users_classes_ref_repo=users_classes_res_repo,
                              class_permission_service=class_permission_service,
                              join_to_class_use_case=join_to_class_uc,
                              class_membership_repo=class_membership_repo)
