from fastapi import Depends

from src.database.repository.school_repository import SchoolRepository, SchoolRepositoryPG
from src.database.repository.users_schools_ref_repository import UsersSchoolsRefRepository, UsersSchoolsRefRepositoryPG
from src.database.repository.school_entry_requests_repository import (SchoolEntryRequestRepository,
                                                                      SchoolEntryRequestRepositoryPG)
from src.database.repository.school_membership_repository import (SchoolMembershipRepository,
                                                                  SchoolMembershipRepositoryPG)

from src.services.school_service import SchoolService
from src.services.use_case.join_to_school_use_case import JoinToSchoolUseCase
from src.services.school_entry_request_service import SchoolEntryRequestService
from src.services.school_permission_service import SchoolPermissionService
from src.services.use_case.send_school_entry_request_use_case import SendSchoolEntryRequestUseCase
from src.services.school_member_service import SchoolMemberService


def get_school_repository() -> SchoolRepository:
    return SchoolRepositoryPG()


def get_users_schools_ref_repository() -> UsersSchoolsRefRepository:
    return UsersSchoolsRefRepositoryPG()


def get_school_entry_requests_repository() -> SchoolEntryRequestRepository:
    return SchoolEntryRequestRepositoryPG()


def get_school_membership_repository() -> SchoolMembershipRepository:
    return SchoolMembershipRepositoryPG()


def get_join_to_school_use_case(
        users_schools_ref_repository: UsersSchoolsRefRepository = Depends(get_users_schools_ref_repository)
) -> JoinToSchoolUseCase:
    return JoinToSchoolUseCase(users_schools_ref_repository)


def get_send_school_entry_request_use_case(
        school_repository: SchoolRepository = Depends(get_school_repository),
        school_entry_requests_repository: SchoolEntryRequestRepository = Depends(get_school_entry_requests_repository),
) -> SendSchoolEntryRequestUseCase:
    return SendSchoolEntryRequestUseCase(school_repository=school_repository,
                                         school_entry_requests_repository=school_entry_requests_repository)


def get_school_permission_service(
        users_schools_ref_repository: UsersSchoolsRefRepository = Depends(get_users_schools_ref_repository)
) -> SchoolPermissionService:
    return SchoolPermissionService(users_schools_ref_repository)


def get_school_service(
        school_repository: SchoolRepository = Depends(get_school_repository),
        users_schools_ref_repository: UsersSchoolsRefRepository = Depends(get_users_schools_ref_repository),
        school_permission_service: SchoolPermissionService = Depends(get_school_permission_service)
) -> SchoolService:
    return SchoolService(school_repository, users_schools_ref_repository, school_permission_service)


def get_school_entry_request_service(
        school_entry_requests_repository: SchoolEntryRequestRepository = Depends(get_school_entry_requests_repository),
        school_permission_service: SchoolPermissionService = Depends(get_school_permission_service),
        join_to_school_use_case: JoinToSchoolUseCase = Depends(get_join_to_school_use_case)
) -> SchoolEntryRequestService:
    return SchoolEntryRequestService(school_entry_requests_repository,
                                     school_permission_service,
                                     join_to_school_use_case)


def get_school_member_service(
        sc_membership_repo: SchoolMembershipRepository = Depends(get_school_membership_repository),
        school_permission_service: SchoolPermissionService = Depends(get_school_permission_service),
        us_ref_repo: UsersSchoolsRefRepository = Depends(get_users_schools_ref_repository)
) -> SchoolMemberService:
    return SchoolMemberService(school_permission_service=school_permission_service,
                               school_membership_repository=sc_membership_repo,
                               users_schools_ref_repo=us_ref_repo)


