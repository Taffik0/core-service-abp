from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, model_validator

from src.dependencies.classes_dependencies import get_class_service
from src.services.class_service import ClassService

from lib.fast_token import require_auth, AuthToken

router = APIRouter()


class CreateClassIn(BaseModel):
    name: str
    class_num: int


@router.get("/schools/{school_id}/classes")
async def get_classes(school_id: int,
                      token: AuthToken = Depends(require_auth),
                      class_service: ClassService = Depends(get_class_service)):
    return await class_service.get_classes(school_id, token.uuid, token.user_type)


@router.get("/classes/{class_id}")
async def get_class(class_id: int,
                    token: AuthToken = Depends(require_auth),
                    class_service: ClassService = Depends(get_class_service)):
    return await class_service.get_class(class_id, token.uuid, token.user_type)


@router.post("/schools/{school_id}/classes")
async def create_class(
        school_id: int,
        class_data: CreateClassIn,
        token: AuthToken = Depends(require_auth),
        class_service: ClassService = Depends(get_class_service)
):
    return await class_service.create_class(user_uuid=token.uuid,
                                            user_role=token.user_type,
                                            school_id=school_id, name=class_data.name,
                                            class_num=class_data.class_num)


@router.delete("/classes/{class_id}")
async def delete_class(
        class_id: int,
        token: AuthToken = Depends(require_auth),
        class_service: ClassService = Depends(get_class_service)
):
    return await class_service.delete_class(class_id, token.uuid, token.user_type)


@router.get("/classes/me")
async def get_class_of_user(
        token: AuthToken = Depends(require_auth),
        class_service: ClassService = Depends(get_class_service)):
    return await class_service.get_classes_of_user(token.uuid)


@router.get("/schools/{school_id}/classes/me")
async def get_class_of_user_and_school(
        school_id: int,
        token: AuthToken = Depends(require_auth),
        class_service: ClassService = Depends(get_class_service)):
    return await class_service.get_classes_of_user_and_school(token.uuid, school_id)
