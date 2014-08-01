from web_server import db, utils


def authorize_user(response, user_id):
    sessionid = str(utils._gen_salt(50))
    db.set_session_data(sessionid, {'user_id' : user_id})
    utils.set_cookie(response, name='sessionid', value=sessionid)
    return response


def get_user_id(request):
    sessionid = get_sessionid_from_cookie(request)
    id_user = get_user_id_by_sessionid(sessionid)
    return id_user


def get_sessionid_from_cookie(request):
    cookies = get_cookies_from_request(request)
    cookies_dict = utils.parsi_cookies_to_dict(cookies)
    if 'sessionid' in cookies_dict:
        sessionid = cookies_dict['sessionid']
    else:
        sessionid = None
    return sessionid


def get_cookies_from_request(request):
    req = request.headers
    if 'Cookie' in req:
        cookies = req['Cookie']
        return cookies
    else:
        cookies = ''
        return cookies


def get_user_id_by_sessionid(sessionid):
    session_data = db.get_data_by_sessionid(sessionid)
    if 'user_id' in session_data:
        user_id = session_data['user_id']
    else:
        user_id = None
    return user_id

def check_user_authorized(request):

    user_id = get_user_id(request)
    if db.check_id_in_db(user_id):
       answer = True
    else:
        answer = False

    return answer
