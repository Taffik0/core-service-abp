from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, model_validator

from lib.fast_token import require_auth, AuthToken

from src.dependencies.school_dependencies import get_school_service
from src.services.school_service import SchoolService

router = APIRouter()


class SchoolCreateIN(BaseModel):
    name: str
    description: str


class SetSchoolRefIN(BaseModel):
    ref: Optional[str] = None
    auto_gen: bool = False

    @model_validator(mode="after")
    def validate_ref(self):
        if not self.auto_gen:
            if not self.ref or len(self.ref) < 10:
                raise ValueError("ref must be at least 10 characters when auto_gen is False")
        return self


class ChangeSchoolIn(BaseModel):
    school_id: int
    name: str | None = None
    description: str | None = None


@router.get("/schools/{school_id}")
async def get_school(
        school_id: int,
        token: AuthToken = Depends(require_auth),
        school_service: SchoolService = Depends(get_school_service)):

    school = await school_service.get_school(token.uuid, token.user_type, school_id)
    return school


@router.get("/schools")
async def get_schools(
        count: int = 20,
        start: int = 0,
        token: AuthToken = Depends(require_auth),
        school_service: SchoolService = Depends(get_school_service)):

    schools = await school_service.get_schools(user_uuid=token.uuid,
                                               user_role=token.user_type,
                                               count=count,
                                               start=start)
    return schools


@router.get("/my-school")
async def get_my_school(token: AuthToken = Depends(require_auth),
                        school_service: SchoolService = Depends(get_school_service)):  # для директоров больше
    schools = await school_service.get_schools_of_user(user_uuid=token.uuid,
                                                       user_role=token.user_type)
    return schools


@router.post("/school")
async def create_my_school(
        school: SchoolCreateIN,
        token: AuthToken = Depends(require_auth),
        school_service: SchoolService = Depends(get_school_service)):
    school_id = await school_service.create_school(token.uuid, token.user_type, school.name, school.description)
    return school_id


@router.patch("/school/{school_id}/ref")
async def set_ref(
        school_id: int,
        ref: SetSchoolRefIN,
        token: AuthToken = Depends(require_auth),
        school_service: SchoolService = Depends(get_school_service)):
    await school_service.set_school_ref(token.uuid, token.user_type, school_id, ref.ref, ref.auto_gen)


@router.patch("/school")
async def change_school(
        change_data: ChangeSchoolIn,
        token: AuthToken = Depends(require_auth),
        school_service: SchoolService = Depends(get_school_service),
):
    await school_service.change_school(user_uuid=token.uuid,
                                       user_role=token.user_type,
                                       school_id=change_data.school_id,
                                       name=change_data.name,
                                       description=change_data.description)


@router.delete("/school/{school_id}")
async def delete_school(
        school_id: int,
        token: AuthToken = Depends(require_auth),
        school_service: SchoolService = Depends(get_school_service),
):
    await school_service.delete_school(user_uuid=token.uuid, user_role=token.user_type, school_id=school_id)
