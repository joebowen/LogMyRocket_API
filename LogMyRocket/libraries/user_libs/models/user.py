import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../../sys_packages"))
sys.path.append(os.path.join(here, "../"))

import uuid
import bcrypt
from boto3.dynamodb.conditions import Key, Attr

from error_handler import UserAlreadyExistsError, UserDoesNotExistError, UsersDoNotExistError, MissingUserIdError, \
    MissingUsernameError, MalformedUserObjectError, MissingUserIdsError, MissingPasswordError


def format_user(user):
    """Format a user JSON object and convert it to a printable format.

        :param user: User object.
        :type user: JSON
        :returns: user
        :rtype: Printable User object

        :raises MissingUserIdError: If 'user_id' is not a key in the user object.
        :raises MissingUsernameError: If 'username' is not a key in the user object.
        :raises MalformedUserObject: If user object is not a dictionary.

    """
    if type(user) is not dict:
        raise MalformedUserObjectError

    if 'user_id' not in user or not user['user_id']:
        raise MissingUserIdError

    if 'username' not in user or not user['username']:
        raise MissingUsernameError

    user = {
        "user_id": user['user_id'],
        "username": user['username']
    }

    return user


def get_one(user_id, users_table):
    """Get a users based on a user id.

        :param user_id: User_id.
        :param users_table: The Users DB table.
        :type user_id: string
        :type users_table: object
        :returns: user
        :rtype: dict

        :raises UserDoesNotExistError: If the user does not exist.
        :raises MissingUserIdError: If user_id is None.

    """
    if not user_id:
        raise MissingUserIdError

    result = users_table.query(KeyConditionExpression=Key('user_id').eq(user_id))

    if not result['Count']:
        raise UserDoesNotExistError

    return format_user(result['Items'][0])


def get_many(user_ids, users_table):
    """Get a users based on a list of user ids.

        :param user_ids: List of user_ids.
        :param users_table: The Users DB table.
        :type user_ids: list
        :type users_table: object
        :returns: user
        :rtype: list

        :raises MissingUserIdsError: If the user_ids list is None.
        :raises UsersDoNotExistError: If not all of the user id's were found in the database.

    """
    if not user_ids:
        raise MissingUserIdsError

    results = users_table.scan(FilterExpression=Attr('user_id').is_in(user_ids))

    if results['Count'] != len(user_ids):
        # Determine which user id's weren't found and include them in the UsersDoNotExistError exception.
        missing_ids = []
        item_ids = [item_id['user_id'] for item_id in results['Items']]
        for missing_id in user_ids:
            if missing_id not in item_ids:
                missing_ids.append(missing_id)

        raise UsersDoNotExistError(missing_ids)

    result_dict = []

    for result in results['Items']:
        result_dict.append(format_user(result))

    return result_dict


def get_all(users_table):
    """Get all the users.

        :param users_table: The Users DB table.
        :type users_table: object
        :returns: user
        :rtype: list

    """
    results = users_table.scan()

    result_dict = []

    for result in results['Items']:
        result_dict.append(format_user(result))

    return result_dict


def create(user, users_table):
    """Create a user.

        :param user: User object.
        :param users_table: The Users DB table.
        :type user: dict
        :type users_table: object

        :raises UserAlreadyExistsError: If the user already exists.
        :raises MissingUsernameError: If the 'username' key is not in event or event['username'] is None.
        :raises MissingPasswordError: If the 'password' key is not in event or event['password'] is None.
        :raises PermissionsError: If the user as defined in the JWT payload is not an admin.

    """
    if 'username' not in user or not user['username']:
        raise MissingUsernameError

    if 'password' not in user or not user['password']:
        raise MissingPasswordError

    check = users_table.scan(FilterExpression=Attr('username').eq(user['username']))

    if check['Count']:
        raise UserAlreadyExistsError

    user['user_id'] = str(uuid.uuid4())

    user['password'] = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())

    user['settings'] = {}
    user['my_motors'] = {}

    user.pop('request', None)

    users_table.put_item(Item=user)

    return user['user_id']


def update(user_id, data, users_table):
    """Update a user with the user id and data to update from.

        :param user_id: User ID.
        :param data: Data to update the user with.
        :param users_table: The Users DB table.
        :type user_id: string
        :type data: JSON
        :type users_table: object

        :raises UserDoesNotExistError: If the user does not exist.
        :raises MissingUserIdError: If the user_id is None.

    """
    if not user_id:
        raise MissingUserIdError

    check = users_table.query(KeyConditionExpression=Key('user_id').eq(user_id))

    if not check['Count']:
        raise UserDoesNotExistError

    if 'password' in data:
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    users_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET username=:username, password=:password, settings=:settings, my_motors=:my_motors',
        ExpressionAttributeValues={
            ':username': data['username'] if 'username' in data else check['Items'][0]['username'],
            ':password': data['password'] if 'password' in data else check['Items'][0]['password'],
            ':settings': data['settings'] if 'settings' in data else check['Items'][0]['settings'],
            ':my_motors': data['my_motors'] if 'my_motors' in data else check['Items'][0]['my_motors'],
        }
    )

    return None


def delete(user_id, users_table):
    """Delete a user with the user id.

        :param user_id: User id.
        :param users_table: The Users DB table.
        :type user_id: string
        :type users_table: object

        :raises UserDoesNotExistError: If the user does not exist.
        :raises MissingUserIdError: If the user_id is None.

    """
    if not user_id:
        raise MissingUserIdError

    check = users_table.query(KeyConditionExpression=Key('user_id').eq(user_id))

    if not check['Count']:
        raise UserDoesNotExistError

    users_table.delete_item(Key={"user_id": user_id})

    return None


def get_by_username(username, users_table):
    """Get a user based on the username.

        :param username: Username.
        :param users_table: The Users DB table.
        :type username: string
        :type users_table: object
        :returns: user
        :rtype: JSON

        :raises UserDoesNotExistError: If the user does not exist.
        :raises MissingUsernameError: If the username is None.

    """
    if not username:
        raise MissingUsernameError

    user = users_table.scan(FilterExpression=Attr('username').eq(username))

    if not user['Count']:
        raise UserDoesNotExistError

    return user['Items'][0]


def add_motor_to_user_collection(motor_id, users_table, payload):
    """Add a motor to a user's collection.

        :param motor_id: Global id of motor to add to the user's collection
        :param users_table: The Users DB table.
        :param payload: Payload from JWT containing authenticated user information.
        :type motor_id: string
        :type users_table: object
        :type payload: json

        :raises UserDoesNotExistError: If the user does not exist.

    """
    check = users_table.query(KeyConditionExpression=Key('user_id').eq(payload['sub']))

    if not check['Count']:
        raise UserDoesNotExistError

    motor_list = check['Items'][0]['my_motors']

    if motor_id in motor_list:
        motor_list[motor_id] += 1
    else:
        motor_list[motor_id] = 1

    users_table.update_item(
        Key={'user_id': payload['sub']},
        UpdateExpression='SET my_motors=:my_motors',
        ExpressionAttributeValues={
            ':my_motors': motor_list
        }
    )

    return None
