from optparse import make_option
from django.core.management.base import NoArgsCommand
from apps.users.management import db


class Command(NoArgsCommand):
    option_list = NoArgsCommand.option_list + (
        make_option('--database', dest='database', default='melafista'),
    )

    def handle_noargs(self, **options):
        db.setup_database(options['database'])
