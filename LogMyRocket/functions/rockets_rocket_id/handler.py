from __future__ import print_function

import logging
import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../libraries/sys_packages"))
sys.path.append(os.path.join(here, "../../libraries/user_libs"))

from database import rockets_table
from models import rocket as rocket_model
from error_handler import UnableToPerformOperationError
from auth import login_check

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
    """Handler for the /rockets/{rocket_id} endpoint.

        ===
        GET
        ===

        Get a JSON object of a rocket model given a rocket id.

        :param event['rocket_id']: Flight id.
        :param event['request']['token']: Requesting client's JWT token.
        :type event['rocket_id']: string
        :type event['request']['token']: string
        :returns flight: Rocket object.
        :rtype: JSON

        :Example:

        curl -X GET -H 'Accept: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' 'http://<server_addr>/rockets/<rocket_id>'

        ===
        PUT
        ===

        Update a rocket given its rocket id.

        :param event['rocket_id']: Rocket id.
        :param event['motor_data']: Rocket model data about flight.
        :param event['request']['token']: Requesting client's JWT token.
        :type event['frocket_id']: string
        :type event['rocket_data']: dict, optional
        :type event['request']['token']: string

        :Example:

        curl -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' -d '{
          "rocket_id": "<string>"
        }' 'http://<server_addr>/rockets/<rocket_id>'

        ======
        DELETE
        ======

        Delete a rocket model given a rocket id.

        :param event['rocket_id']: Rocket id.
        :param event['request']['token']: Requesting client's JWT token.
        :type event['rocket_id']: string
        :type event['request']['token']: string

        :Example:

        curl -X DELETE -H 'Accept: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' 'http://<server_addr>/rockets/<rocket_id>'

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    payload = login_check(event)

    http_method = event['request']['http_method']

    if http_method == 'GET':
        rocket = rocket_model.get_one(event['rocket_id'], rockets_table, payload)

        return rocket

    elif http_method == 'PUT':
        rocket_model.update(event['flight_id'], event, rockets_table)

        return None

    elif http_method == 'DELETE':
        rocket_model.delete(event['flight_id'], rockets_table)

        return None

    raise UnableToPerformOperationError
