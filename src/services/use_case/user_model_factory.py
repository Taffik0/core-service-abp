from pydantic import ValidationError
from src.models.user.user_types_in import UserBaseTypeIn, USER_IN_TYPE_MAP, UserIn, UserTypeIn
from src.models.user.user_type_enum import UserTypes


class UserInModelFactory:
    def create_user_model_in(self, data: dict) -> UserIn | None:
        user_base = self._parse_base_model_in(data)
        if not user_base:
            return None
        user_type = UserTypes(user_base.type)
        data["user_uuid"] = user_base.uuid

        user_base_type = self._parse_model_in(USER_IN_TYPE_MAP[user_type], data)
        if not user_base_type:
            return None
        user = UserIn(user_base, [user_base_type])
        return user

    def _parse_base_model_in(self, data: dict) -> UserBaseTypeIn | None:
        try:
            return UserBaseTypeIn.model_validate(data)
        except ValidationError:
            return None

    def _parse_model_in(self, user_type: type[UserTypeIn], data: dict) -> UserTypeIn | None:
        try:
            return user_type.model_validate(data)
        except ValidationError:
            return None
