from fastapi import APIRouter, Request, UploadFile, File, Depends, Cookie
from fastapi.responses import JSONResponse

from lib.fast_token import authorize_user, get_uuid_of_token

from src.services.users_avatars_service import add_avatar


router = APIRouter()


@router.patch("patch-avatar", dependencies=[Depends(authorize_user)])
async def patch_avatar(request: Request, avatar: UploadFile = File(...), jwt: str = Cookie(None)):
    user_uuid = get_uuid_of_token(jwt)
    if not avatar.content_type.startswith("image/"):
        return JSONResponse({"error": "Неверный тип файла"}, status_code=400)

    await add_avatar(user_uuid, avatar)
