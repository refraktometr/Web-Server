from django.shortcuts import redirect, render_to_response
from functools import wraps
import json
from apps.users import models
from melafista import utils


SESSION_KEY = 'sessionid'
SESSION_ID_LEN = 50


def _generate_sessionid():
    return utils.get_random_string(length=SESSION_ID_LEN)


def authorize_user(response, user_id):
    session_id = _generate_sessionid()
    models.Session.objects.create(session_id, {'user_id': user_id})
    response.set_cookie(key=SESSION_KEY, value=session_id, max_age=None)
    return response


def get_user_id(request):
    session_id = request.COOKIES.get(SESSION_KEY)

    if not session_id:
        return

    session = models.Session.objects.get(session_id)

    if session:
        return session.data.get('user_id')


def logout_user(request, response):
    session_id = request.COOKIES.get(SESSION_KEY)
    models.Session.objects.delete(session_id)
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
