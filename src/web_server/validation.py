from web_server.db import get_user_by_username


def validate_username(username):
    errors = []

    if not username:
        errors.append("Enter username")

    if not errors and len(username) < 3:
        errors.append("Username is too short")

    if not errors and get_user_by_username(username):
        errors.append("User already exists")

    return errors

def validate_password(password):
    errors =[]

    if not password:
        errors.append("Enter password")

    if not errors and len(password) < 5:
        errors.append("Password is to short")

    return errors
