import hashlib
import random
import string
import unittest2


def _gen_salt(length=25):
    return ''.join(random.choice(string.hexdigits) for _ in range(length))


def get_hash_with_salt(_string):
    salt = _gen_salt()
    return get_hash(_string + salt), salt


def get_hash(_string):
    return hashlib.sha256(_string).hexdigest()


def _parse_cookies_to_dict(cookies):
    cookies = cookies.split(';')
    for i in range(len(cookies)):
        cookies[i] = cookies[i].strip()

    cookies_dict = {}
    for i in cookies:
        if '=' in i:
            key, value = i.split('=')
            cookies_dict[key] = value

    return cookies_dict


class BaseTestCase(unittest2.TestCase):
    def setUp(self):
        from web_server import db
        db.truncate_users()


def set_cookie(response, name, value, expires='Thu, 01 Jan 2070 00:00:00 GMT'):
    cookie = '{}={}; expires={}; '
    response.headers['Set-cookie'] = cookie.format(name, value, expires)
    return


def delete_cookie(response, name):
    set_cookie(response, name, value='deleted', expires='Thu, 01 Jan 1970 00:00:00 GMT')


def get_cookie_value(request, cookie_key, default=None):
    cookies = request.headers.get('Cookie', '')
    cookies_dict = _parse_cookies_to_dict(cookies)
    return cookies_dict.get(cookie_key, default)
