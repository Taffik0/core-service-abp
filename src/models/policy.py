from dataclasses import dataclass

from src.models.user.user_type_enum import UserTypes

ConditionName = str


@dataclass(frozen=True)
class Policy:
    roles: set[UserTypes]
    condition: ConditionName | None = None
