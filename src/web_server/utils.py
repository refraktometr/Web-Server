import hashlib
import random
import string
import unittest2
from flask import Flask, request


def _gen_salt(length=25):
    return ''.join(random.choice(string.hexdigits) for _ in range(length))


def get_hash_with_salt(_string):
    salt = _gen_salt()
    return get_hash(_string + salt), salt


def get_hash(_string):
    return hashlib.sha256(_string).hexdigest()


def get_sessionid(request):
    req = request.headers
    cookies = req['Cookie']
    cookies = cookies.split(';')
    for i in range(len(cookies)):
        cookies[i] = cookies[i].strip()
    for i in cookies:
        d = {}
        k = i.split('=')
        d[k[0]] = k[1]
    sessionid = d['sessionid']
    return sessionid


class BaseTestCase(unittest2.TestCase):
    def setUp(self):
        from web_server import db
        db.truncate_users()
