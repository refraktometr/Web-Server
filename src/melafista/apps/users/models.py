import json
from melafista import utils

class Session(object):
    def __init__(self, sessionid, data, create_at):
        self.id = sessionid
        self.data = json.loads(data)
        self.create_at = create_at


class User(object):
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
