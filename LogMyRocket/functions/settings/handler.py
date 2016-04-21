from __future__ import print_function

import logging
import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../libraries/sys_packages"))
sys.path.append(os.path.join(here, "../../libraries/user_libs"))

from database import users_table
from auth import login_check
from models import user as user_model
from error_handler import UnableToPerformOperationError

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
    """Handler for the /settings endpoint.

        ===
        GET
        ===

        Get a JSON object of the current user settings.

        :param event['request']['token']: Requesting client's JWT token.
        :type event['request']['token']: string
        :returns settings: A json object of the current user settings.
        :rtype: JSON

        :Example:

        curl -X GET -H 'Authorization: Bearer <JWT_TOKEN>' -H 'Cache-Control: no-cache' 'https://<server_addr>/settings'

        ===
        PUT
        ===

        Updates user settings using HTTP PUT.

        Parameters are given in the JSON object of the http PUT call.

        :param event['settings']: User settings to update.
        :param event['request']['token']: Requesting client's JWT token.
        :type event['settings']: string
        :type event['request']['token']: string

        :Example:

        curl -X POST -H 'Authorization: Bearer <JWT_TOKEN>'
            -H 'Content-Type: application/json'
            -H 'Accept: application/json'
            -d '{
              "settings": "<string>"
            }' 'http://<server_addr>/settings'

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    payload = login_check(event)

    http_method = event['request']['http_method']

    if http_method == 'GET':
        settings = user_model.get_user_settings(users_table, payload)

        return settings

    elif http_method == 'PUT':
        user_model.set_user_settings(event['settings'], users_table, payload)

        return None

    raise UnableToPerformOperationError
