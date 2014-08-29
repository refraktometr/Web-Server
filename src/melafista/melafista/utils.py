import hashlib
import random
import string


DEFAULT_COOKIE_DATE = 'Thu, 01 Jan 2070 00:00:00 GMT'
EXPIRED_DATE = 'Thu, 01 Jan 1970 00:00:00 GMT'
SALT_LENGTH = 32
SESSION_KEY = 'sessoinid'

def get_random_string(length):
    return ''.join(random.choice(string.hexdigits) for _ in range(length))


def get_hash_with_salt(_string, salt=None):
    if salt is None:
        salt = get_random_string(length=SALT_LENGTH)
    return get_hash(_string + salt), salt


def get_hash(_string):
    return hashlib.sha256(_string).hexdigest()
