from __future__ import print_function

import logging
import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../libraries/sys_packages"))
sys.path.append(os.path.join(here, "../../libraries/user_libs"))

from database import rockets_table
from auth import login_check
from models import rocket as rocket_model
from error_handler import UnableToPerformOperationError

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
    """Handler for the /rockets endpoint.

        ===
        GET
        ===

        Get a JSON object of all users.

        :param event['request']['token']: Requesting client's JWT token.
        :type event['request']['token']: string
        :returns rockets: A list of the rockets to be returned.
        :rtype: JSON

        :Example:

        curl -X GET -H 'Authorization: Bearer <JWT_TOKEN>' -H 'Cache-Control: no-cache' 'https://<server_addr>/rockets'


        ====
        POST
        ====

        Create a rocket model using HTTP POST.

        Parameters are given in the JSON object of the http POST call.

        :param event['rocket_data']: Data of the rocket model to create.
        :param event['request']['token']: Requesting client's JWT token.
        :type event['rocket_data']: string
        :type event['request']['token']: string

        :Example:

        curl -X POST -H 'Authorization: Bearer <JWT_TOKEN>'
            -H 'Content-Type: application/json'
            -H 'Accept: application/json'
            -d '{
              "rocket_data": <dict>
            }' 'http://<server_addr>/rockets'

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    payload = login_check(event)

    http_method = event['request']['http_method']

    if http_method == 'GET':
        rockets = rocket_model.get_all(rockets_table, payload)

        return rockets

    elif http_method == 'POST':
        event.pop("request", None)
        rocket_id = rocket_model.create(event, rockets_table, payload)

        return {'rocket_id': rocket_id}

    raise UnableToPerformOperationError
