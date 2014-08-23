from django.conf import settings
from django_nose import NoseTestSuiteRunner
from apps.users.management import db


class TestRunner(NoseTestSuiteRunner):
    def setup_databases(self):
        settings.DATABASES['default']['NAME'] = 'test_melafista'
        db.setup_database('test_melafista')

    def teardown_databases(self, *args, **kwargs):
        db.delete_database('test_melafista')
