from fastapi import APIRouter

from src.routers import (user_api, avatars_api,
                         class_ref_api, teacher_api,
                         school_api, school_members_api,
                         classes_api, class_members_api)

ROUTERS_LIST = [user_api, avatars_api, class_ref_api,
                teacher_api, school_api, school_members_api,
                classes_api, class_members_api]

routers = APIRouter()

for router in ROUTERS_LIST:
    routers.include_router(router.router)
