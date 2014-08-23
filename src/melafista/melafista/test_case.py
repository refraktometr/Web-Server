from django.conf import settings
from unittest2 import TestCase as BaseTestCase
from apps.users.management import db


class TestCase(BaseTestCase):
    def run(self, result=None):
        super(TestCase, self).run(result=result)
        db.flush_tables(settings.DATABASES['default']['NAME'])