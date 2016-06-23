from __future__ import print_function

import logging
import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../libraries/sys_packages"))
sys.path.append(os.path.join(here, "../../libraries/user_libs"))

sys.path.append(os.path.join(here, "libraries/sys_packages"))
sys.path.append(os.path.join(here, "libraries/user_libs"))

from database import users_table
from models import user as user_model
from database import rockets_table
from models import rocket as rocket_model

from error_handler import UnableToPerformOperationError

log = logging.getLogger()
log.setLevel(logging.DEBUG)


def handler(event, context):
    """Handler for the /signup endpoint.

        ====
        POST
        ====

        Sign-up and create a user using HTTP POST.

        Parameters are given in the JSON object of the http POST call.

        :param event['username']: User name of the user to create.
        :param event['password']: Password of the user to create.
        :param event['settings']: List of settings to add to the user being created.
        :type event['username']: string
        :type event['password']: string
        :type event['settings']: list of dicts

        :Example:

        curl -X POST -H 'Content-Type: application/json'
            -H 'Accept: application/json'
            -d '{
              "username": "string",
              "password": "string",
              "settings": [
                {"key", "value"}
              ],
            }' 'http://<server_addr>/signup'

        :raises UnableToPerformOperationError: If an invalid http_method is used to call the endpoint handler.

    """
    if 'request' not in event:
        raise UnableToPerformOperationError

    http_method = event['request']['http_method']

    if http_method == 'POST':
        event.pop("request", None)
        user_id = user_model.create(event, users_table)

        event = {
            "rocket_data": {
                "colors": "Silver, Blue",
                "mfg": "Estes",
                "motors": [
                  [
                    {
                      "diameter": "13"
                    }
                  ]
                ],
                "name": "Gnome",
                "notes": "Recommended Motors: 1/2A3-2T, 1/2A3-4T, A3-4T, A10-3T",
                "preflight": [
                  "Insert wadding",
                  "Roll up streamer, insert into body tube and insert nose cone",
                  "Insert motor",
                  "Insert motor starter and secure with plug"
                ],
                "recovery": "Streamer",
                "rod": "1/8\""
            }
        }

        payload = {
            'sub' : user_id
        }

        rocket_model.create(event, rockets_table, payload)

        return {"user_id": user_id}

    raise UnableToPerformOperationError
