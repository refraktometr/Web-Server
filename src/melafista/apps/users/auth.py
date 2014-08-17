from django.shortcuts import redirect, render_to_response
from functools import wraps
import json
from apps.users import db, utils

def authorize_user(response, user_id):
    sessionid = str(utils._gen_salt(50))
    db.set_session_data(sessionid, {'user_id' : user_id})
    utils.set_cookie(response, name='sessionid', value=sessionid)
    return response


def get_user_id(request):
    sessionid = utils.get_cookie_value(request, cookie_key='sessionid')

    if not sessionid:
        return

    _, raw_data, _ = db.get_session_data(sessionid)
    session_data = json.loads(raw_data)

    if session_data:
        return session_data.get('user_id')


def logout_user(request, response):
    sessionid = utils.get_cookie_value(request, cookie_key='sessionid')
    db.del_session(sessionid)
    utils.delete_cookie(response, 'sessionid')
    return response


def check_authorization(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user_id = get_user_id(request)

        if user_id:
            kwargs['user_id'] = user_id
            response = func(request, *args, **kwargs)
        else:
            response = redirect('/')
        return response

    return wrapper
