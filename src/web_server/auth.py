from web_server import db, utils




def authorize_user(response, user_id):
    sessionid = str(utils._gen_salt(50))
    db.set_session_data(sessionid, {'user_id' : user_id})
    cookie = 'sessionid=' + sessionid
    response.headers['Set-cookie'] = cookie
    return response

def get_sessionid_from_cookie(request):
    req = request.headers
    cookies = req['Cookie']
    cookies_dict = utils.parsi_cookies_to_dict(cookies)
    sessionid = cookies_dict['sessionid']
    return sessionid

def get_user_id(request):
    sessionid = get_sessionid_from_cookie(request)
    id_user = db.get_user_id_by_sessionid(sessionid)
    return id_user

