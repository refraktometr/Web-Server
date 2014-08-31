import json

class Session:
    def __init__(self, sessionid, data, create_at):
        self.id = sessionid
        self.data = json.loads(data)
        self.create_at = create_at

class User:
    def __init__(self, id, name, password, salt):
        self.id = id
        self.name = name
        self.password = password
        self.salt = salt