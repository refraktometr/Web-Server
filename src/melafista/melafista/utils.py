import hashlib
import random
import string


COOKIE_KEY = 'Thu, 01 Jan 2070 00:00:00 GMT'

def _gen_salt(length=32):
    return ''.join(random.choice(string.hexdigits) for _ in range(length))


def get_hash_with_salt(_string, salt=None):
    if salt is None:
        salt = _gen_salt()
    return get_hash(_string + salt), salt


def get_hash(_string):
    return hashlib.sha256(_string).hexdigest()


def set_cookie(response, name, value, expires=COOKIE_KEY):
    response.set_cookie(key=name, value=value, expires=expires)


def delete_cookie(response, name):
    set_cookie(response, name, value='deleted', expires=COOKIE_KEY)


def get_cookie_value(request, cookie_key, default=None):
    cookies = request.COOKIES
    return cookies.get(cookie_key, default)
