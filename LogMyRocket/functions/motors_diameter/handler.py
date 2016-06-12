from __future__ import print_function

import logging
import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../libraries/sys_packages"))
sys.path.append(os.path.join(here, "../../libraries/user_libs"))

import requests
import xmltodict

from error_handler import UnableToPerformOperationError
from auth import login_check

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
    """Handler for the /motors/diameter/{diameter} endpoint.

        ===
        GET
        ===

        Get more information about motors given the motor diameter.

        :param event['diameter']: Motor Diameter.
        :param event['request']['token']: Requesting client's JWT token.
        :type event['diameter']: string
        :type event['request']['token']: string
        :returns motors: Motor objects.
        :rtype: JSON

        :Example:

        curl -X GET -H 'Accept: application/json' -H 'Authorization: Bearer <JWT_TOKEN>' 'http://<server_addr>/motors/diameter/<diameter>'

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    payload = login_check(event)

    http_method = event['request']['http_method']

    if http_method == 'GET':
        url = "http://www.thrustcurve.org/servlets/search"
        request_data = '<search-request>' \
                       '    <diameter>' + event['diameter'] + '</diameter>' \
                       '    <max-results>2000</max-results>' \
                       '</search-request>'

        rawmotors = xmltodict.parse(requests.post(url, data=request_data).text)

        allmotors = {}

        for motor in rawmotors['search-response']['results']['result']:
            if motor['diameter'] not in allmotors:
                allmotors[motor['diameter']] = []

            allmotors[motor['diameter']].append(motor)

        return allmotors

    raise UnableToPerformOperationError
