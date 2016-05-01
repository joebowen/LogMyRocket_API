from __future__ import print_function

import sys
import os

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../sys_packages"))
sys.path.append(os.path.join(here, "../"))

import uuid
from boto3.dynamodb.conditions import Key, Attr

from error_handler import FlightAlreadyExistsError, FlightDoesNotExistError, FlightsDoNotExistError, \
    MissingUserIdError, MissingFlightIdError, MissingFlightIdsError, MalformedFlightObjectError, MissingRocketDataError


def get_one(flight_id, flights_table, payload):
    """Get a flight based on a flight_id.

        :param flight_id: Flight id.
        :param flights_table: The Flights DB table.
        :param payload: Dictionary of the JWT payload claim set.
        :type flight_id: string
        :type flights_table: object
        :type payload: dict
        :returns: flight
        :rtype: dict

        :raises FlightDoesNotExistError: If the flight does not exist.
        :raises MissingFlightIdError: If flight_id is None.

    """
    if not flight_id:
        raise MissingFlightIdError

    result = flights_table.query(KeyConditionExpression=Key('flight_id').eq(flight_id),
                                 FilterExpression=Attr('owner').eq(payload['sub']))

    if not result['Count']:
        raise FlightDoesNotExistError

    return result['Items'][0]


def get_many(flight_ids, flights_table, payload):
    """Get flights based on a list of flight ids.

        :param flight_ids: List of flight ids.
        :param flights_table: The Flights DB table.
        :param payload: Dictionary of the JWT payload claim set.
        :type flight_ids: list
        :type flights_table: object
        :type payload: dict
        :returns: flight
        :rtype: list

        :raises MissingFlightIdsError: If the flight_ids list is None.
        :raises FlightsDoNotExistError: If not all of the flight id's were found in the database.

    """
    if not flight_ids:
        raise MissingFlightIdsError

    results = flights_table.scan(FilterExpression=Attr('flight_id').is_in(flight_ids) &
                                                  Attr('owner').eq(payload['sub']))

    if results['Count'] != len(flight_ids):
        # Determine which flight ids weren't found and include them in the FlightsDoNotExistError exception.
        missing_ids = []
        item_ids = [item_id['flight_id'] for item_id in results['Items']]
        for missing_id in flight_ids:
            if missing_id not in item_ids:
                missing_ids.append(missing_id)

        raise FlightsDoNotExistError(missing_ids)

    result_dict = []

    for result in results['Items']:
        result_dict.append(result)

    return result_dict


def get_all(flights_table, payload):
    """Get all the flights.

        :param flights_table: The Flights DB table.
        :param payload: Dictionary of the JWT payload claim set.
        :type flights_table: object
        :type payload: dict
        :returns: flight
        :rtype: list

    """
    results = flights_table.scan(FilterExpression=Attr('owner').eq(payload['sub']))

    result_dict = []

    for result in results['Items']:
        result_dict.append(result)

    return result_dict


def create(flight, flights_table, payload):
    """Create a flight.

        :param flight: Flight object.
        :param flights_table: The Flights DB table.
        :param payload: Dictionary of the JWT payload claim set.
        :type flight: dict
        :type flights_table: object
        :type payload: dict

        :raises MissingUserIdError: If 'sub' is not a key in the payload object.
        :raises MissingRocketDataError: If 'rocket_data' is not a key in the flight object.

    """
    if 'sub' not in payload or not payload['sub']:
        raise MissingUserIdError

    if 'rocket_data' not in flight or not flight['rocket_data']:
        raise MissingRocketDataError

    flight['owner'] = payload['sub']

    flight['flight_id'] = str(uuid.uuid4())

    flights_table.put_item(Item=flight)

    return flight['flight_id']


def update(flight_id, data, flights_table):
    """Update a flight with the flight id and data to update from.

        :param flight_id: Flight ID.
        :param data: Data to update the flight with.
        :param flights_table: The Flights DB table.
        :type flight_id: string
        :type data: JSON
        :type flights_table: object

        :raises FlightDoesNotExistError: If the flight does not exist.
        :raises MissingFlightIdError: If the flight_id is None.

    """
    if not flight_id:
        raise MissingFlightIdError

    check = flights_table.query(KeyConditionExpression=Key('flight_id').eq(flight_id))

    if not check['Count']:
        raise FlightDoesNotExistError

    flights_table.update_item(
        Key={'flight_id': flight_id},
        UpdateExpression='SET rocket_id=:rocket_id, motor_data=:motor_data, flight_data=:flight_data',
        ExpressionAttributeValues={
            ':rocket_id': data['rocket_id'] if 'rocket_id' in data else check['Items'][0]['rocket_id'],
            ':motor_data': data['motor_data'] if 'motor_data' in data else check['Items'][0]['motor_data'],
            ':flight_data': data['flight_data'] if 'flight_data' in data else check['Items'][0]['flight_data'],
        }
    )

    return None


def delete(flight_id, flights_table):
    """Delete a flight with the flight id.

        :param flight_id: Flight id.
        :param flights_table: The Flights DB table.
        :type flight_id: string
        :type flights_table: object

        :raises FlightDoesNotExistError: If the flight does not exist.
        :raises MissingFlightIdError: If the flight_id is None.

    """
    if not flight_id:
        raise MissingFlightIdError

    check = flights_table.query(KeyConditionExpression=Key('flight_id').eq(flight_id))

    if not check['Count']:
        raise FlightDoesNotExistError

    flights_table.delete_item(Key={"flight_id": flight_id})

    return None
