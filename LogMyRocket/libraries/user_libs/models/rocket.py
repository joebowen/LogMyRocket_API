from __future__ import print_function

import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../sys_packages"))
sys.path.append(os.path.join(here, "../"))

import uuid
from boto3.dynamodb.conditions import Key, Attr

from error_handler import MissingRocketIdError, RocketDoesNotExistError, MissingRocketIdsError, \
    RocketsDoNotExistError, MissingUserIdError


def get_one(rocket_id, rockets_table, payload):
    """Get a rocket model based on a rocket_id.

        :param rocket_id: Rocket model id.
        :param rockets_table: The Rockets DB table.
        :param payload: Dictionary of the JWT payload claim set.
        :type rocket_id: string
        :type rockets_table: object
        :type payload: dict
        :returns: rocket
        :rtype: dict

        :raises RocketDoesNotExistError: If the rocket does not exist.
        :raises MissingRocketIdError: If rocket_id is None.

    """
    if not rocket_id:
        raise MissingRocketIdError

    result = rockets_table.query(KeyConditionExpression=Key('rocket_id').eq(rocket_id),
                                 FilterExpression=Attr('owner').eq(payload['sub']))

    if not result['Count']:
        raise RocketDoesNotExistError

    return result['Items'][0]


def get_many(rocket_ids, rockets_table, payload):
    """Get rockets based on a list of rocket ids.

        :param rocket_ids: List of rocket ids.
        :param rockets_table: The Rockets DB table.
        :param payload: Dictionary of the JWT payload claim set.
        :type rocket_ids: list
        :type rockets_table: object
        :type payload: dict
        :returns: rocket
        :rtype: list

        :raises MissingRocketIdsError: If the rocket_ids list is None.
        :raises RocketsDoNotExistError: If not all of the rocket id's were found in the database.

    """
    if not rocket_ids:
        raise MissingRocketIdsError

    results = rockets_table.scan(FilterExpression=Attr('rocket_id').is_in(rocket_ids) &
                                                  Attr('owner').eq(payload['sub']))

    if results['Count'] != len(rocket_ids):
        # Determine which rocket ids weren't found and include them in the RocketsDoNotExistError exception.
        missing_ids = []
        item_ids = [item_id['rocket_id'] for item_id in results['Items']]
        for missing_id in rocket_ids:
            if missing_id not in item_ids:
                missing_ids.append(missing_id)

        raise RocketsDoNotExistError(missing_ids)

    result_dict = []

    for result in results['Items']:
        result_dict.append(result)

    return result_dict


def get_all(rockets_table, payload):
    """Get all the rockets.

        :param rockets_table: The Rockets DB table.
        :param payload: Dictionary of the JWT payload claim set.
        :type rockets_table: object
        :type payload: dict
        :returns: flight
        :rtype: list

    """
    results = rockets_table.scan(FilterExpression=Attr('owner').eq(payload['sub']))

    result_dict = []

    for result in results['Items']:
        result_dict.append(result)

    return result_dict


def create(rocket, rockets_table, payload):
    """Create a rocket model.

        :param rocket: Rocket model object.
        :param rockets_table: The Flights DB table.
        :param payload: Dictionary of the JWT payload claim set.
        :type rocket: dict
        :type rockets_table: object
        :type payload: dict

        :raises MissingUserIdError: If 'sub' is not a key in the payload object.
        :raises MissingRocketIdError: If 'rocket_id' is not a key in the flight object.

    """
    if 'sub' not in payload or not payload['sub']:
        raise MissingUserIdError

    rocket['owner'] = payload['sub']

    rocket['rocket_id'] = str(uuid.uuid4())

    rockets_table.put_item(Item=rocket)

    return rocket['rocket_id']


def update(rocket_id, data, rockets_table):
    """Update a rocket model with the rocket id and data to update from.

        :param rocket_id: Rocket ID.
        :param data: Data to update the rocket with.
        :param rockets_table: The Rockets DB table.
        :type rocket_id: string
        :type data: JSON
        :type rockets_table: object

        :raises RocketDoesNotExistError: If the rocket does not exist.
        :raises MissingRocketIdError: If the rocket_id is None.

    """
    if not rocket_id:
        raise MissingRocketIdError

    check = rockets_table.query(KeyConditionExpression=Key('rocket_id').eq(rocket_id))

    if not check['Count']:
        raise RocketDoesNotExistError

    rockets_table.update_item(
        Key={'rocket_id': rocket_id},
        UpdateExpression='SET rocket_data=:rocket_data',
        ExpressionAttributeValues={
            ':rocket_data': data['rocket_data'] if 'rocket_data' in data else check['Items'][0]['rocket_data']
        }
    )

    return None


def delete(rocket_id, rockets_table):
    """Delete a rocket model with the rocket id.

        :param rocket_id: Rocket id.
        :param rockets_table: The Rockets DB table.
        :type rocket_id: string
        :type rockets_table: object

        :raises RocketDoesNotExistError: If the rocket does not exist.
        :raises MissingRocketIdError: If the rocket_id is None.

    """
    if not rocket_id:
        raise MissingRocketIdError

    check = rockets_table.query(KeyConditionExpression=Key('rocket_id').eq(rocket_id))

    if not check['Count']:
        raise RocketDoesNotExistError

    rockets_table.delete_item(Key={"rocket_id": rocket_id})

    return None
