from fastapi import APIRouter, Request, Cookie, Depends
from lib.fast_token import authorize_user, get_uuid_of_token

from src.database import user_db_obj
from src.models.users import Student

from src.dependencies.dependencies import get_class_ref_service, get_class_repository
from src.services.class_ref_service import ClassRefService
from src.database.repository.class_repository import ClassRepository

router = APIRouter()


@router.get("/get-class")
async def get_class(request: Request, ref: str,
                    class_repository: ClassRepository= Depends(get_class_repository)):
    school_class = await class_repository.get_class_by_ref(ref)
    if school_class:
        return school_class.dict()
    return None


@router.post("/join-to-class", dependencies=[Depends(authorize_user)])
async def join_to_class(request: Request, ref: str, jwt: str = Cookie(None),
                        class_ref_service: ClassRefService = Depends(get_class_ref_service),
                        class_repository: ClassRepository= Depends(get_class_repository)):
    uuid = get_uuid_of_token(jwt)
    print(f"{uuid=}")
    user = await user_db_obj.get_user_data(uuid)
    school_class = await class_repository.get_class_by_ref(ref)
    if not school_class:
        return "wrong class"
    if not isinstance(user, Student):
        return "you are not student"
    user.class_id = school_class.id
    user.class_num = school_class.class_num
    user.school_id = school_class.school_id
    await class_repository.set_class_to_student(school_class.id, uuid)  # обновление базы
    await class_ref_service.send_join_to_class(user)  # отправка в брокер
    return "ok"
