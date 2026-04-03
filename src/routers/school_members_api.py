from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from uuid import UUID

from lib.fast_token import require_auth, AuthToken

from src.logger import logger

from src.services.school_entry_request_service import SchoolEntryRequestService
from src.services.use_case.send_school_entry_request_use_case import SendSchoolEntryRequestUseCase
from src.services.school_member_service import SchoolMemberService
from src.services.student_service import StudentService
from src.services.teacher_service import TeacherService
from src.dependencies.school_dependencies import (get_school_entry_request_service,
                                                  get_send_school_entry_request_use_case,
                                                  get_school_member_service)
from src.dependencies.user_dependecies import get_teacher_service, get_student_service

router = APIRouter()


class SendEntryRequestIN(BaseModel):
    school_ref: str


@router.get("/schools/{school_id}/entry-requests")
async def get_entry_requests(
        school_id: int,
        token: AuthToken = Depends(require_auth),
        school_members_service: SchoolEntryRequestService = Depends(get_school_entry_request_service)
):
    return await school_members_service.get_entry_requests(school_id, token.uuid, token.user_type)


@router.get("/schools/entry-requests/{request_id}")
async def get_entry_request(
        request_id: int,
        token: AuthToken = Depends(require_auth),
        req_service: SchoolEntryRequestService = Depends(get_school_entry_request_service)
):
    return await req_service.get_entry_request(request_id, token.uuid, token.user_type)


@router.post("/schools/entry_requests")
async def send_entry_request(
        send_entry_request_in: SendEntryRequestIN,
        token: AuthToken = Depends(require_auth),
        send_school_entry_request_use_case: SendSchoolEntryRequestUseCase =
        Depends(get_send_school_entry_request_use_case)
):
    await send_school_entry_request_use_case.send_school_request(send_entry_request_in.school_ref, token.uuid)


@router.post("/schools/entry_requests/{request_id}/submit")
async def submit_entry_request(
        request_id: int,
        token: AuthToken = Depends(require_auth),
        req_service: SchoolEntryRequestService = Depends(get_school_entry_request_service)
):
    await req_service.submit_entry_request(request_id, token.uuid, token.user_type)


@router.post("/schools/entry_requests/{request_id}/reject")
async def reject_entry_request(
        request_id: int,
        token: AuthToken = Depends(require_auth),
        req_service: SchoolEntryRequestService = Depends(get_school_entry_request_service)
):
    await req_service.reject_entry_request(request_id, token.uuid, token.user_type)


@router.get("/schools/{school_id}/students")
async def get_students(
        school_id: int,
        start: int = 0,
        count: int = 40,
        token: AuthToken = Depends(require_auth),
        sc_members_service: SchoolMemberService = Depends(get_school_member_service)):
    return await sc_members_service.get_students(school_id, token.uuid, token.user_type, start=start, count=count)


@router.get("/schools/students/{student_uuid}")
async def get_student(
        student_uuid: UUID,
        token: AuthToken = Depends(require_auth),
        student_service: StudentService = Depends(get_student_service)):
    return await student_service.get_student(student_uuid)


@router.get("/schools/{school_id}/teachers")
async def get_teachers(
        school_id: int,
        start: int = 0,
        count: int = 40,
        token: AuthToken = Depends(require_auth),
        sc_members_service: SchoolMemberService = Depends(get_school_member_service)
):
    logger.info("fff")
    return await sc_members_service.get_teachers(school_id, token.uuid, token.user_type, start=start, count=count)


@router.get("/schools/teachers/{teacher_uuid}")
async def get_teacher(
        teacher_uuid: UUID,
        token: AuthToken = Depends(require_auth),
        teacher_service: TeacherService = Depends(get_teacher_service)
):
    return await teacher_service.get_teacher(teacher_uuid=teacher_uuid)


@router.delete("/schools/{school_id}/members/{member_uuid}")
async def get_teacher(
        school_id: int,
        member_uuid: UUID,
        token: AuthToken = Depends(require_auth),
        sc_members_service: SchoolMemberService = Depends(get_school_member_service)
):
    return await sc_members_service.delete_ref(token.uuid, token.user_type, member_uuid, school_id)
