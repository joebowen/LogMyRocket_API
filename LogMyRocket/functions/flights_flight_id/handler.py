from __future__ import print_function

import logging
import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../libraries/sys_packages"))
sys.path.append(os.path.join(here, "../../libraries/user_libs"))

from database import flights_table
from models import flight as flight_model
from error_handler import UnableToPerformOperationError
from auth import login_check

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
    """Handler for the /flights/{flight_id} endpoint.

        ===
        GET
        ===

        Get a JSON object of a flight given a flight id.

        :param event['flight_id']: Flight id.
        :param event['request']['token']: Requesting client's JWT token.
        :type event['flight_id']: string
        :type event['request']['token']: string
        :returns flight: Flight object.
        :rtype: JSON

        :Example:

        curl -X GET -H 'Accept: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' 'http://<server_addr>/flights/<flight_id>'

        ===
        PUT
        ===

        Update a flight given its flight id.

        :param event['flight_id']: Flight id.
        :param event['model_id']: ID of rocket model to attach to flight.
        :param event['motor_data']: Motor data about flight.
        :param event['flight_data']: Flight data about flight.
        :param event['request']['token']: Requesting client's JWT token.
        :type event['flight_id']: string
        :type event['model_id']: string, optional
        :type event['motor_data']: dict, optional
        :type event['flight_data']: dict, optional
        :type event['request']['token']: string

        :Example:

        curl -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' -d '{
          "flight_id": "<string>"
        }' 'http://<server_addr>/flights/<flight_id>'

        ======
        DELETE
        ======

        Delete a flight given a flight id.

        :param event['flight_id']: Flight id.
        :param event['request']['token']: Requesting client's JWT token.
        :type event['flight_id']: string
        :type event['request']['token']: string

        :Example:

        curl -X DELETE -H 'Accept: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' 'http://<server_addr>/flights/<flight_id>'

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    payload = login_check(event)

    http_method = event['request']['http_method']

    if http_method == 'GET':
        flight = flight_model.get_one(event['flight_id'], flights_table, payload)

        return flight

    elif http_method == 'PUT':
        flight_model.update(event['flight_id'], event, flights_table)

        return None

    elif http_method == 'DELETE':
        flight_model.delete(event['flight_id'], flights_table)

        return None

    raise UnableToPerformOperationError
