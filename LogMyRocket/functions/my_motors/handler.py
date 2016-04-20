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
from auth import login_check

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
    """Handler for the /my_motors endpoint.

        ===
        GET
        ===

        Get a JSON object of all of the motors in the user collection.

        :param event['request']['token']: Requesting client's JWT token.
        :type event['request']['token']: string
        :rtype: JSON

        :Example:

        curl -X GET -H 'Accept: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' 'http://<server_addr>/my_motors

        ===
        PUT
        ===

        Add a motor to the user collection.

        :param event['motor_id']: ID of motor to add to the collection.
        :param event['request']['token']: Requesting client's JWT token.
        :type event['motor_id']: string
        :type event['request']['token']: string

        :Example:

        curl -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' -d '{
          "motor_id": "<string>"
        }' 'http://<server_addr>/flights/<flight_id>'

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    payload = login_check(event)

    http_method = event['request']['http_method']

    if http_method == 'GET':
        user = user_model.get_one(payload['sub'], users_table, payload)

        return user['my_motors']

    elif http_method == 'PUT':
        user_model.add_motor_to_user_collection(event['motor_id'], users_table, payload)

        return None

    raise UnableToPerformOperationError
