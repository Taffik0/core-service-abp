from enum import Enum

from src.models.policy import Policy
from src.models.user.user_type_enum import UserTypes


class SchoolScope(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    TEACHERS = "teachers"
    STUDENTS = "students"
    MEMBERS = "members"
    CLASSES = "classes"
    ENTRY_REQUEST = "entry_request"


class PermissionAction(Enum):
    READ = "read"
    WRITE = "write"
    MANAGE = "manage"


POLICIES: dict[tuple[SchoolScope, PermissionAction], Policy] = {
    (SchoolScope.PUBLIC, PermissionAction.READ): Policy(
        roles={UserTypes.STUDENT, UserTypes.TEACHER, UserTypes.DIRECTOR}
    ),

    (SchoolScope.INTERNAL, PermissionAction.READ): Policy(
        roles={UserTypes.TEACHER, UserTypes.DIRECTOR}
    ),

    (SchoolScope.INTERNAL, PermissionAction.WRITE): Policy(
        roles={UserTypes.DIRECTOR}
    ),

    (SchoolScope.CLASSES, PermissionAction.WRITE): Policy(
        roles={UserTypes.TEACHER},
    ),

    (SchoolScope.ENTRY_REQUEST, PermissionAction.READ): Policy(
        roles={UserTypes.DIRECTOR},
    ),
    (SchoolScope.ENTRY_REQUEST, PermissionAction.WRITE): Policy(
        roles={UserTypes.DIRECTOR},
    ),

    (SchoolScope.TEACHERS, PermissionAction.READ): Policy(
        roles={UserTypes.DIRECTOR},
    ),
    (SchoolScope.TEACHERS, PermissionAction.WRITE): Policy(
        roles={UserTypes.DIRECTOR},
    ),

    (SchoolScope.STUDENTS, PermissionAction.READ): Policy(
        roles={UserTypes.DIRECTOR},
    ),
    (SchoolScope.STUDENTS, PermissionAction.WRITE): Policy(
        roles={UserTypes.DIRECTOR},
    ),

    (SchoolScope.MEMBERS, PermissionAction.READ): Policy(
        roles={UserTypes.DIRECTOR},
    ),
    (SchoolScope.MEMBERS, PermissionAction.WRITE): Policy(
        roles={UserTypes.DIRECTOR},
    ),

    (SchoolScope.CLASSES, PermissionAction.READ): Policy(
        roles={UserTypes.DIRECTOR},
    ),
    (SchoolScope.CLASSES, PermissionAction.WRITE): Policy(
        roles={UserTypes.DIRECTOR},
    ),
}

