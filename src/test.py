from src.models.user.user_fabric import create_user_by_dict
from src.utils import user_sql_generator

if __name__ == "__main__":
    data =  {'username': 'Test03',
             'firstname': 'ttt',
             'surname': 'ttt',
             'thirdname': 'ttt',
             'nickname': 'ttt',
             'uuid': 'd301780d-82e2-4907-a05e-1fb88aa95cbc',
             'type': 'student'}
    user = create_user_by_dict(data)
    print(user.get_tables())
    print(user_sql_generator.build_tables_insert_sql(user.get_tables()))

