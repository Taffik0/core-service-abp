from enum import Enum

from src.models.policy import Policy
from src.models.user.user_type_enum import UserTypes


class ClassScope(Enum):
    PUBLIC = "public"
    REF = "ref"
    MEMBERS = "members"
    TEACHERS = "teachers"
    STUDENTS = "students"


class PermissionAction(Enum):
    READ = "read"
    WRITE = "write"
    MANAGE = "manage"


POLICIES: dict[tuple[ClassScope, PermissionAction], Policy] = {
    (ClassScope.PUBLIC, PermissionAction.READ): Policy(
        roles={UserTypes.STUDENT, UserTypes.TEACHER, UserTypes.DIRECTOR}
    ),

    (ClassScope.PUBLIC, PermissionAction.WRITE): Policy(
        roles={UserTypes.DIRECTOR}
    ),

    (ClassScope.REF, PermissionAction.READ): Policy(
        roles={UserTypes.TEACHER, UserTypes.DIRECTOR}
    ),

    (ClassScope.REF, PermissionAction.WRITE): Policy(
        roles={UserTypes.DIRECTOR, UserTypes.TEACHER}
    ),

    (ClassScope.MEMBERS, PermissionAction.READ): Policy(
        roles={UserTypes.TEACHER, UserTypes.DIRECTOR, UserTypes.STUDENT}
    ),

    (ClassScope.MEMBERS, PermissionAction.WRITE): Policy(
        roles={UserTypes.DIRECTOR}
    ),

    (ClassScope.TEACHERS, PermissionAction.READ): Policy(
        roles={UserTypes.TEACHER, UserTypes.DIRECTOR, UserTypes.STUDENT}
    ),

    (ClassScope.TEACHERS, PermissionAction.WRITE): Policy(
        roles={UserTypes.DIRECTOR}
    ),

    (ClassScope.STUDENTS, PermissionAction.READ): Policy(
        roles={UserTypes.TEACHER, UserTypes.DIRECTOR, UserTypes.STUDENT}
    ),

    (ClassScope.STUDENTS, PermissionAction.WRITE): Policy(
        roles={UserTypes.DIRECTOR, UserTypes.TEACHER}
    ),
}

