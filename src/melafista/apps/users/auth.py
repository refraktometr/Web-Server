from django.shortcuts import redirect, render_to_response
from functools import wraps
import json
from apps.users import db as user_db
from melafista import utils


SESSION_KEY = 'sessionid'
SESSION_ID_LEN = 50


def _generate_sessionid():
    return utils.get_random_string(length=SESSION_ID_LEN)


def authorize_user(response, user_id):
    sessionid = _generate_sessionid()
    user_db.create_session_data(sessionid, {'user_id': user_id})
    response.set_cookie(key=SESSION_KEY, value=sessionid, max_age=None)
    return response


def get_user_id(request):
    sessionid = request.COOKIES.get(SESSION_KEY)

    if not sessionid:
        return

    session = user_db.get_session(sessionid)

    if session:
        return session.data.get('user_id')


def logout_user(request, response):
    sessionid = request.COOKIES.get(SESSION_KEY)
    user_db.del_session(sessionid)
    response.delete_cookie(key=SESSION_KEY)
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
