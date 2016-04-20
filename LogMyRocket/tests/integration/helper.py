import os, sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../functions"))

from functions.auth import handler as auth_handler


def login_test_user():
    """Log in test user to bypass authentication."""
    login_info = {
        "request": {
            "http_method": "POST",
            "path": "/auth"
        },
        "username": "testing_admin",
        "password": "password"
    }

    rv = auth_handler.handler(login_info, None)

    return rv
