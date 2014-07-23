from web_server import db, utils


def authorize_user(username, password):
    user_information = db.get_user_by_username(username)

    if not user_information:
        return False

    _, _, user_password, salt = user_information
    return user_password == utils.get_hash(password + salt)

def set_session_key(response):
    ssesionid = 'ssesionid=' + str(utils._gen_salt(50))
    response.headers['Set-cookie'] = ssesionid
    return response