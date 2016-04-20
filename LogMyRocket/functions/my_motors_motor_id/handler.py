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
    """Handler for the /motors/{motor_id} endpoint.

        ===
        GET
        ===

        Get a JSON object of a motor given a motor id.

        :param event['motor_id']: Motor id.
        :param event['request']['token']: Requesting client's JWT token.
        :type event['motor_id']: string
        :type event['request']['token']: string
        :returns flight: Motor object.
        :rtype: JSON

        :Example:

        curl -X GET -H 'Accept: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' 'http://<server_addr>/my_motors/<motor_id>'

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    payload = login_check(event)

    http_method = event['request']['http_method']

    if http_method == 'GET':
        motor = motor_model.get_one(event['motor_id'])

        return motor

    raise UnableToPerformOperationError
