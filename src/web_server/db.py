import psycopg2

from web_server import utils
import json

conn_string = "host='localhost' dbname='web_server' user='postgres' password='postgres'"


def get_cursor():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    conn.autocommit = True
    return cursor


def get_users():
    cursor = get_cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


def truncate_users():
    cursor = get_cursor()
    cursor.execute("TRUNCATE TABLE users")


def create_user(username, password):
    cursor = get_cursor()

    password, salt = utils.get_hash_with_salt(password)

    query = "INSERT INTO users(username, password, salt) VALUES (%s, %s, %s) RETURNING id;"
    cursor.execute(query, (username, password, salt))
    return cursor.fetchone()[0]

def get_valid_user(username, password):
    user_information = get_user_by_username(username)

    if not user_information:
        return False

    user_id, _, user_password, salt = user_information
    if user_password == utils.get_hash(password + salt):
        return user_id
    else:
        return False


def get_user_by_username(username):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", [username])
    return cursor.fetchone()


def get_user_by_user_id(user_id):
     cursor = get_cursor()
     cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
     return cursor.fetchone()

def set_session_data(sessionid, data):
    cursor = get_cursor()
    data = json.dumps(data)
    query = "INSERT INTO sessions(sessionid, data) VALUES (%s, %s);"
    cursor.execute(query, (sessionid, data))
    return


def get_user_id_by_sessionid(sessionid):
    user_information = get_data_by_sessionid(sessionid)
    _, data = user_information
    data = json.loads(data)
    user_id = data['user_id']
    return user_id


def get_data_by_sessionid(sessionid):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM sessions WHERE sessionid = %s", [sessionid])
    return cursor.fetchone()
