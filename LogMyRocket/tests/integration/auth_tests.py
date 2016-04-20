import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../functions"))
sys.path.append(os.path.join(here, "../libraries/user_libs"))
sys.path.append(os.path.join(here, "../libraries/sys_packages"))

from helper import login_test_user

from functions.auth import handler as auth_handler
from functions.users import handler as user_handler


def test_user_auth():
    """Test user authentication."""
    data = {
        "request": {
            "http_method": "POST",
            "path": "/users"
        },
        "username": "test_user",
        "password": "password",
    }

    rv = login_test_user()

    data['request']['token'] = "Bearer " + rv['token']

    user_handler.handler(data, None)

    login_info = {
        "request": {
            "http_method": "POST",
            "path": "/auth"
        },
        "username": "test_user",
        "password": "password"
    }

    rv = auth_handler.handler(login_info, None)

    assert 'token' in rv


