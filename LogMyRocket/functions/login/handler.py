from __future__ import print_function

import logging
from datetime import datetime, timedelta
import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../libraries/sys_packages"))
sys.path.append(os.path.join(here, "../../libraries/user_libs"))

import jwt
import bcrypt

from auth import jwt_secret
from database import users_table
from models import user as user_model
from error_handler import UserAuthError, UnableToPerformOperationError, MissingUsernameError, MissingPasswordError

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
    """Handler for the /login endpoint.

        ====
        POST
        ====

        Given successful login information this returns a JWT token in JSON format as well as attaches the
        token to the session object.

        Parameters are given in the JSON object of the http POST call.

        :param event['username']: Username.
        :param event['password']: Password
        :type event['username']: string
        :type event['password']: string
        :returns: `{'token': <token>}`
        :rtype: JSON

        :raises MissingUsernameError: If the 'username' key is not in event or event['username'] is None.
        :raises MissingPasswordError: If the 'password' key is not in event or event['password'] is None.
        :raises UserAuthError: If error occurs on user authentication.

        :Example:

        curl -X POST -H 'Content-Type: application/json' -d '{
            "username": "<string>",
            "password": "<string>"
        }' "https://<server_addr>/login"

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    http_method = event['request']['http_method']

    if http_method == 'POST':
        if 'username' not in event or not event['username']:
            raise MissingUsernameError

        if 'password' not in event or not event['password']:
            raise MissingPasswordError

        try:
            user = user_model.get_by_username(event['username'], users_table)

            if bcrypt.hashpw(event['password'].encode('utf-8'), user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                payload = {
                    'exp': datetime.utcnow() + timedelta(minutes=30),
                    'nbf': datetime.utcnow(),
                    'iat': datetime.utcnow(),
                    'sub': user['user_id'],
                    'iss': 'www.logmyrocket.info',
                    'settings': user['settings']
                }

                token = jwt.encode(payload, jwt_secret)
            else:
                raise UserAuthError

        except Exception as exp:
            log.error(exp)
            raise UserAuthError

        return {'token': token}

    raise UnableToPerformOperationError
