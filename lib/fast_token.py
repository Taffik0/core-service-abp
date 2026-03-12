"""Эта библиотека отвечает за работу с токенами авторизации"""
from fastapi import Request, HTTPException, Depends
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError
from uuid import UUID

SECRET_KEY = "my_super_secret_key"
ALGORITHM = "HS256"


class AuthToken:
    def __init__(self, uuid: UUID, user_type: str, exp: int):
        self.uuid = uuid
        self.user_type = user_type
        self.exp = exp


def authorize_user(request: Request):
    token = request.cookies.get("jwt")
    print(token)
    if not token:
        raise HTTPException(status_code=401, detail="auth token missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="no id in auth token")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="invalid auth token")


def require_auth(request: Request) -> AuthToken:
    token = request.cookies.get("jwt")
    if not token:
        raise HTTPException(status_code=401, detail="auth token missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_uuid = UUID(payload["sub"])
        user_type = payload["type"]
        exp = payload["exp"]

        return AuthToken(
            uuid=user_uuid,
            user_type=user_type,
            exp=int(exp),
        )

    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="auth token expired")
    except JWTError:
        raise HTTPException(status_code=401, detail="invalid auth token")


def make_token(auth_data: dict) -> AuthToken:
    user_uuid = UUID(auth_data.get("sub"))
    exp = int(auth_data.get("exp"))
    user_type = auth_data.get("type")
    if user_uuid and user_type and exp:
        return AuthToken(uuid=user_uuid, user_type=user_type, exp=exp)


def get_uuid_of_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            return None
        return user_id
    except Exception as e:
        print(e)