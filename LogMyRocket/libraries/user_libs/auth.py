import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../sys_packages"))

import jwt
import logging
from error_handler import AuthRequiredError, InvalidTokenError

# TODO: Fix this. This secret should be stored elsewhere.
jwt_secret = "TESTSECRETKEY"

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def login_check(event):
    """Used to verify a login token in the request object to access an API end point.

        :param event: HTTP Event.
        :param event['request']['token']: Requesting client's JWT token.
        :type event: object
        :type event['request']['token']: string

        :returns payload: Dictionary of the JWT payload claim set.
        :rtype payload: dict

        :raises AuthRequiredError: If the token is not included in the request.
        :raises InvalidTokenError: If there is a problem decoding the token, which can happen for several reasons;
            malformed token, token that doesn't verify with the jwt_secret, expired token, etc.

    """

    if 'token' not in event['request']:
        raise AuthRequiredError

    try:
        # Using [7:] strips off "Bearer " from the token.
        payload = jwt.decode(event['request']['token'][7:], jwt_secret)
    except jwt.InvalidTokenError as jwt_exp:
        log.error(jwt_exp)
        raise InvalidTokenError

    return payload
