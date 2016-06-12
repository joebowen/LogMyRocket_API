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
    """Handler for the /my_motors/{motor_id} endpoint.

        ======
        DELETE
        ======

        Remove a motor from the user's motor collection.

        :param event['motor_id']: Motor id.
        :param event['request']['token']: Requesting client's JWT token.
        :type event['motor_id']: string
        :type event['request']['token']: string

        :Example:

        curl -X DELETE -H 'Accept: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' 'http://<server_addr>/my_motors/<motor_id>'

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    payload = login_check(event)

    http_method = event['request']['http_method']

    if http_method == 'DELETE':
        user_model.del_motor_from_user_collection(event['motor_id'], users_table, payload)

        return None

    raise UnableToPerformOperationError
