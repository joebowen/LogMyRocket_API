from __future__ import print_function

import logging
import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../libraries/sys_packages"))
sys.path.append(os.path.join(here, "../../libraries/user_libs"))

from auth import login_check
from error_handler import UnableToPerformOperationError

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
    """Handler for the /verify endpoint.

        ===
        GET
        ===

        Verify a JWT token.

        :param event['request']['token']: Requesting client's JWT token.
        :type event['request']['token']: string
        :returns verified: A boolean value.  "true" if the JWT token is valid.
        :rtype: string

        :Example:

        curl -X GET -H 'Authorization: Bearer <JWT_TOKEN>' -H 'Cache-Control: no-cache' 'https://<server_addr>/verify'

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    payload = login_check(event)

    http_method = event['request']['http_method']

    if http_method == 'GET':
        return "true"

    raise UnableToPerformOperationError
