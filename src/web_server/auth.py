import hashlib
from web_server.db import get_user_by_username



def authorization_user(username, password):

    user_information = get_user_by_username(username)
    password = hashlib.sha256(password + user_information[3]).hexdigest()
    if user_information[2] == password:
        return (True)
    else:
        return (False)
