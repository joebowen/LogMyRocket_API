import os, sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../functions"))
sys.path.append(os.path.join(here, "../../libraries/user_libs"))
sys.path.append(os.path.join(here, "../libraries/sys_packages"))

from mock import patch

from functions.login.handler import handler


def test_login_handler_post_basic():
    """Test calling the /login handler with a POST http call."""
    event = {
        "request": {
            "http_method": "POST",
            "path": "/auth"
        },
        "username": "test_user",
        "password": "password"
    }

    user_return = {
        "user_id": 'test_user_id',
        "username": 'username'
    }

    with patch('models.user.get_by_username', return_value=user_return):
        return_val = handler(event, None)

    assert 'token' in return_val

