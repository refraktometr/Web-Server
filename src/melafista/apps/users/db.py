import json
from melafista import utils, base_db
from apps.users import models


def create_user(username, password):
    password, salt = utils.get_hash_with_salt(password)

    query = "INSERT INTO users(username, password, salt) VALUES (%s, %s, %s) RETURNING id;"
    return base_db.fetchone(query, username, password, salt)[0]


def get_valid_user(username, password):
    user = get_user(username=username)

    if not user:
        return

    if user.password == utils.get_hash(password + user.salt):
        return user.id
    else:
        return


def get_user(user_id=None, username=None):
    user = None
    if user_id:
        query = "SELECT * FROM users WHERE id = %s"
        fetched_data = base_db.fetchone(query, user_id)
        if fetched_data:
            user = models.User(*fetched_data)

    if username:
        query = "SELECT * FROM users WHERE username = %s"
        fetched_data = base_db.fetchone(query, username)
        if fetched_data:
            user = models.User(*fetched_data)

    return user



def create_session_data(session_id, data):
    data = json.dumps(data)
    query = "INSERT INTO sessions(session_id, data) VALUES (%s, %s);"
    base_db.execute(query, session_id, data)


def get_session(sessionid):

    raw_data = base_db.fetchone("SELECT * FROM sessions WHERE session_id = %s", sessionid)

    if raw_data:
        session = models.Session(*raw_data)
        return session



def del_session(sessionid):
    base_db.execute("DELETE FROM sessions WHERE session_id = %s", sessionid)


def get_id_and_username_all_users():
    return base_db.fetchall(query="SELECT id, username FROM users")
