import psycopg2
import json
from django.conf import settings
from melafista import utils, base_db


def create_user(username, password):
    password, salt = utils.get_hash_with_salt(password)

    query = "INSERT INTO users(username, password, salt) VALUES (%s, %s, %s) RETURNING id;"
    return base_db.fetchone(query, username, password, salt)[0]


def get_valid_user(username, password):
    user_information = get_user_by_username(username)

    if not user_information:
        return

    user_id, _, user_password, salt = user_information
    if user_password == utils.get_hash(password + salt):
        return user_id
    else:
        return


def get_user_by_username(username):
    query = "SELECT * FROM users WHERE username = %s"
    return base_db.fetchone(query, username)


def get_user_by_user_id(user_id):
    return base_db.fetchone("SELECT * FROM users WHERE id = %s", user_id)


def set_session_data(session_id, data):
    cursor = base_db.get_cursor()
    data = json.dumps(data)
    query = "INSERT INTO sessions(session_id, data) VALUES (%s, %s);"
    cursor.execute(query, (session_id, data))


def get_session_data(sessionid):
    return base_db.fetchone("SELECT * FROM sessions WHERE session_id = %s", sessionid)


def del_session(sessionid):
    cursor = base_db.get_cursor()
    cursor.execute("DELETE FROM sessions WHERE session_id = %s", [sessionid])


def get_id_and_username_all_users():
    return base_db.fetchall(query="SELECT id, username FROM users")
