import psycopg2
import json
from apps.users import utils


def get_cursor():
    conn = psycopg2.connect("host='localhost' dbname='melafista' user='postgres' password='postgres'")
    cursor = conn.cursor()
    conn.autocommit = True
    return cursor


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


def set_session_data(session_id, data):
    cursor = get_cursor()
    data = json.dumps(data)
    query = "INSERT INTO sessions(session_id, data) VALUES (%s, %s);"
    cursor.execute(query, (session_id, data))
    return


def get_session_data(sessionid):
    cursor = get_cursor()
    cursor.execute("SELECT * FROM sessions WHERE session_id = %s", [sessionid])
    return cursor.fetchone()


def del_session(sessionid):
    cursor = get_cursor()
    cursor.execute("DELETE FROM sessions WHERE session_id = %s", [sessionid])


def get_id_and_username_all_users():
    cursor = get_cursor()
    cursor.execute("SELECT id, username FROM users")
    return cursor.fetchall()
