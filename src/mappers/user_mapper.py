from src.models.user.user_types_in import (UserBaseTypeIn, StudentTypeIn, DirectorTypeIn,
                                           TeacherTypeIn, AdminTypeIn, UserIn)
from src.models.user.user_types import (UserBaseType, StudentType, DirectorType,
                                        TeacherType, AdminType, User)


def _map_user_base(user_base: UserBaseTypeIn) -> UserBaseType:
    return UserBaseType(
        uuid=user_base.uuid,
        nickname=user_base.nickname,
        firstname=user_base.firstname,
        surname=user_base.surname,
        thirdname=user_base.thirdname,
        type=user_base.type)


def _map_student(student_in: StudentTypeIn) -> StudentType:
    return StudentType(
        user_uuid=student_in.uuid,
        class_id=student_in.class_id,
        class_num=student_in.class_num)


def _map_teacher(teacher_in: TeacherTypeIn) -> TeacherType:
    return TeacherType(user_uuid=teacher_in.uuid, subject_id=teacher_in.subject_id)


def _map_director(director_in: DirectorTypeIn) -> DirectorType:
    return DirectorType(user_uuid=director_in.uuid)


def _map_admin(admin_in: AdminTypeIn) -> AdminType:
    return AdminType(user_uuid=admin_in.uuid, privileges=admin_in.privileges)


USER_TYPES_MAP = {
    UserBaseTypeIn: _map_user_base,
    StudentTypeIn: _map_student,
    TeacherTypeIn: _map_teacher,
    DirectorTypeIn: _map_director,
    AdminTypeIn: _map_admin
}


def map_user(user_in: UserIn) -> User:
    user_base = _map_user_base(user_in.user_base)

    user_types = []
    for user_type in user_in.users_types:
        mapper = USER_TYPES_MAP.get(type(user_type))
        if mapper is None:
            raise ValueError(f"Unknown user type: {type(user_type)}")

        user_types.append(mapper(user_type))

    return User(user_base=user_base, users_types=user_types)
