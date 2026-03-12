import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(database="usersDatadb", user="postgres", password="Qyz]vrcJX>m04[",host="localhost")
cur = conn.cursor(cursor_factory=RealDictCursor)



def add_user(data):
    uuid = data["uuid"]
    firstname = data["firstname"]
    surname = data["surname"]
    thirdname = data["thirdname"]
    nickname = data["nickname"]
    cur.execute("""INSERT INTO users (uuid, firstname, surname, thirdname, nickname) Values (%s, %s, %s, %s, %s)""",(uuid, firstname, surname, thirdname, nickname))
    conn.commit()

def get_user_data(uuid, data_names = None):
    select_data = "*"
    if data_names != None:
        data_names_str = ",".join(str(name) for name in data_names)
        select_data = data_names_str

    cur.execute(f"SELECT {select_data} FROM users Where uuid = %s",(uuid,))
    user_data = cur.fetchone()
    print(user_data)
    if data_names == None:
        user_data.pop("uuid")
    return user_data

if __name__ == "__main__":
    cur.execute("SELECT * FROM users")
    print(cur.fetchall())
