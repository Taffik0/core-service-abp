from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, model_validator
from uuid import UUID

from lib.fast_token import require_auth, AuthToken

from src.services.class_permission_service import ClassPermissionService
from src.dependencies.classes_dependencies import (get_class_member_service,
                                                   get_join_to_class_use_case,
                                                   get_join_to_class_by_ref_use_case)
from src.services.class_members_service import ClassMemberService
from src.services.use_case.join_to_class_use_case import JoinToClassUseCase
from src.services.use_case.join_to_class_by_ref_use_case import JoinToClassByRefUseCase

router = APIRouter()


class JoinToClassByRefIn(BaseModel):
    ref: str


@router.get("classes/{class_id}/students")
async def get_student_of_class(
        class_id: int,
        token: AuthToken = Depends(require_auth),
        class_member_serv: ClassMemberService = Depends(get_class_member_service)):
    return await class_member_serv.get_students_of_class(token.uuid, token.user_type, class_id)


@router.get("classes/{class_id}/teachers")
async def get_student_of_class(
        class_id: int,
        token: AuthToken = Depends(require_auth),
        class_member_serv: ClassMemberService = Depends(get_class_member_service)):
    return await class_member_serv.get_teacher_of_class(token.uuid, token.user_type, class_id)


@router.post("classes/{class_id}/members/{member_uuid}")
async def appoint_member(
        class_id: int, member_uuid: UUID,
        token: AuthToken = Depends(require_auth),
        class_member_serv: ClassMemberService = Depends(get_class_member_service)):
    return await class_member_serv.appoint_members(token.uuid, token.user_type, member_uuid, class_id)

@router.post("classes/join")
async def jon_to_class_by_ref(
        ref_in: JoinToClassByRefIn,
        token: AuthToken = Depends(require_auth),
        join_to_class_by_ref_uc: JoinToClassByRefUseCase = Depends(get_join_to_class_by_ref_use_case)
):
    return await join_to_class_by_ref_uc.join(token.uuid, ref_in.ref)

