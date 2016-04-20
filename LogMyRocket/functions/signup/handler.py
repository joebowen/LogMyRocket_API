from __future__ import print_function

import logging
import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../libraries/sys_packages"))
sys.path.append(os.path.join(here, "../../libraries/user_libs"))

from database import users_table
from models import user as user_model

from error_handler import UnableToPerformOperationError

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
    """Handler for the /signup endpoint.

        ====
        POST
        ====

        Sign-up and create a user using HTTP POST.

        Parameters are given in the JSON object of the http POST call.

        :param event['username']: User name of the user to create.
        :param event['password']: Password of the user to create.
        :type event['username']: string
        :type event['password']: string

        :Example:

        curl -X POST -H 'Content-Type: application/json'
            -H 'Accept: application/json'
            -d '{
              "username": "string",
              "password": "string"
            }' 'http://<server_addr>/signup'

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    http_method = event['request']['http_method']

    if http_method == 'POST':
        user_id = user_model.create(event, users_table)

        return {user_id}

    raise UnableToPerformOperationError
