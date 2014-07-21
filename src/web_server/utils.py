import hashlib
import random
import string


def _gen_salt(length=25):
    return ''.join(random.choice(string.hexdigits) for _ in range(length))


def get_hash_with_salt(_string):
    salt = _gen_salt()
    return get_hash(_string + salt), salt


def get_hash(_string):
    return hashlib.sha256(_string).hexdigest()
