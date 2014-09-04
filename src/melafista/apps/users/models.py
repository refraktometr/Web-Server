import json
from melafista import utils, base_db
from orm.models import Manager, Model


class SessionManager(Manager):
    def create(self, session_id, data):
        query = "INSERT INTO sessions(session_id, data) VALUES (%s, %s);"
        base_db.execute(query, session_id, json.dumps(data))
        create_at = base_db.fetchone("SELECT create_at FROM sessions WHERE session_id = %s", session_id)
        return Session(session_id, data, create_at)

    def get(self, session_id):
        raw_data = base_db.fetchone("SELECT * FROM sessions WHERE session_id = %s", session_id)

        if raw_data:
            session_id, data, create_at = raw_data
            data = json.loads(data)
            session = Session(session_id, data, create_at)
            return session

    def delete(self, session_id):
        base_db.execute("DELETE FROM sessions WHERE session_id = %s", session_id)


class Session(Model):
    objects = SessionManager()

    def __init__(self, sessionid, data, create_at):
        self.id = sessionid
        self.data = data
        self.create_at = create_at


class UserManager(Manager):
    def create(self, username, password):
        password, salt = utils.get_hash_with_salt(password)

        query = "INSERT INTO users(username, password, salt) VALUES (%s, %s, %s) RETURNING id;"
        user_id = base_db.fetchone(query, username, password, salt)
        return self.model(user_id[0], username, password, salt)

    def get(self, user_id=None, username=None):
        user = None
        if user_id:
            query = "SELECT * FROM users WHERE id = %s"
            fetched_data = base_db.fetchone(query, user_id)
            if fetched_data:
                user = User(*fetched_data)

        if username:
            query = "SELECT * FROM users WHERE username = %s"
            fetched_data = base_db.fetchone(query, username)
            if fetched_data:
                user = User(*fetched_data)

        return user

    def all(self):
        users_data = base_db.fetchall(query="SELECT * FROM users")
        users = []
        for data in users_data:
            user = User(*data)
            users.append(user)
        return users


class User(Model):
    objects = UserManager()
    def __init__(self, id, username, password, salt):
        self.id = id
        self.username = username
        self.password = password
        self.salt = salt

    def check_password(self, raw_password):
        if self.password == utils.get_hash(raw_password + self.salt):
            return True
        else:
            return False
