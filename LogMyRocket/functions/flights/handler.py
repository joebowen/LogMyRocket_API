from __future__ import print_function

import logging
import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../libraries/sys_packages"))
sys.path.append(os.path.join(here, "../../libraries/user_libs"))

from database import flights_table
from auth import login_check
from models import flight as flight_model
from error_handler import UnableToPerformOperationError

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
    """Handler for the /flights endpoint.

        ===
        GET
        ===

        Get a JSON object of all flights.

        :param event['request']['token']: Requesting client's JWT token.
        :type event['request']['token']: string
        :returns flights: A list of the flights to be returned.
        :rtype: JSON

        :Example:

        curl -X GET -H 'Authorization: Bearer <JWT_TOKEN>' -H 'Cache-Control: no-cache' 'https://<server_addr>/flights'


        ====
        POST
        ====

        Create a flight using HTTP POST.

        Parameters are given in the JSON object of the http POST call.

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

        curl -X POST -H 'Authorization: Bearer <JWT_TOKEN>'
            -H 'Content-Type: application/json'
            -H 'Accept: application/json'
            -d '{
              "name": "<string>"
            }' 'http://<server_addr>/flights'

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    payload = login_check(event)

    http_method = event['request']['http_method']

    if http_method == 'GET':
        flights = flight_model.get_all(flights_table, payload)

        return flights

    elif http_method == 'POST':
        flight_id = flight_model.create(event, flights_table, payload)

        return {'flight_id': flight_id}

    raise UnableToPerformOperationError
