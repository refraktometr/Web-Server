from django.shortcuts import redirect, render_to_response
from functools import wraps
import json
from apps.users import db as user_db
from melafista import utils

SESSION_KEY='sessoinid'

def authorize_user(response, user_id):
    sessionid = str(utils._gen_salt(50))
    user_db.create_session_data(sessionid, {'user_id' : user_id})
    utils.set_cookie(response, name=SESSION_KEY, value=sessionid)
    return response


def get_user_id(request):
    sessionid = utils.get_cookie_value(request, cookie_key=SESSION_KEY)

    if not sessionid:
        return

    session_data = user_db.get_session_data(sessionid)

    if session_data:
        return session_data.get('user_id')


def logout_user(request, response):
    sessionid = utils.get_cookie_value(request, cookie_key=SESSION_KEY)
    user_db.del_session(sessionid)
    utils.delete_cookie(response, SESSION_KEY)
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
