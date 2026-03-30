from fastapi import APIRouter, Request, Cookie, Depends
from uuid import UUID

from cachetools import TTLCache

from pydantic import BaseModel, conlist

from lib.fast_token import authorize_user, get_uuid_of_token
from lib.fast_token import require_auth, AuthToken

from src.services import main_data_service
from src.logger import logger
from src.dependencies.user_dependecies import get_user_service
from src.services.users_service import UsersService, UserUpdateDTO

router = APIRouter()


user_cache = TTLCache(maxsize=1000, ttl=30)


class UserBulkIn(BaseModel):
    uuids: conlist(UUID, min_length=1, max_length=100)


class UserPatchIn(BaseModel):
    nickname: str | None
    firstname: str | None
    surname: str | None
    thirdname: str | None


@router.get("/get-data", dependencies=[Depends(authorize_user)])
async def get_user_data(request: Request, data_name: str = None, jwt: str = Cookie(None)):
    uuid = get_uuid_of_token(jwt)
    return await main_data_service.get_main_data(uuid, data_name)


@router.get("/get-data/{user_id}")
async def get_not_me_user_data(user_id: str):
    return {"message": f"Данные пользователя {user_id}"}


@router.post("/users/bulk")
async def get_user_by_uuids(
        user_batch: UserBulkIn,
        token: AuthToken = Depends(require_auth),
        user_service: UsersService = Depends(get_user_service)):
    return await user_service.get_users_by_uuids(user_batch.uuids)


@router.get("/users/me")
async def get_user_by_jwt(token: AuthToken = Depends(require_auth),
                          user_service: UsersService = Depends(get_user_service)):
    # if token.uuid in user_cache:
    #    return user_cache[token.uuid]
    user = await user_service.get_user(token.uuid)
    user_cache[token.uuid] = user
    return user


@router.get("/users/{user_uuid}")
async def get_user(user_uuid: UUID, token: AuthToken = Depends(require_auth),
                   user_service: UsersService = Depends(get_user_service)):
    return await user_service.get_user(user_uuid)


@router.patch("/users/me")
async def patch_user_by_jwt(
        user_update_in: UserPatchIn,
        token: AuthToken = Depends(require_auth),
        user_service: UsersService = Depends(get_user_service)):
    user_upd_data = UserUpdateDTO(nickname=user_update_in.nickname,
                                  firstname=user_update_in.firstname,
                                  surname=user_update_in.surname,
                                  thirdname=user_update_in.thirdname)
    return await user_service.update_user(token.uuid, user_upd_data)
