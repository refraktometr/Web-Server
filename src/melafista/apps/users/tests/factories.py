from apps.users import models
from melafista import utils


def create_user(username=None, password=None):
    if not username:
        username = str(utils.get_random_string(30))

    if not password:
        password = str(utils.get_random_string(30))

    user = models.User.objects.create(username, password)
    return user