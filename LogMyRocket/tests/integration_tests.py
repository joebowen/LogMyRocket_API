import os, sys

os.environ['TESTING'] = "true"

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../libraries/sys_packages"))
sys.path.append(os.path.join(here, "../libraries/user_libs"))

from database import users_table, rockets_table, flights_table
from models import user as user_model

# Import tests
from integration.auth_tests import *


def setup_function(function):
    delete_all_items(users_table)
    delete_all_items(rockets_table)
    delete_all_items(flights_table)
    create_init_user()


def delete_all_items(table):
    """Deletes all items from a DynamoDB table."""
    keys = [k['AttributeName'] for k in table.key_schema]
    response = table.scan()
    items = response['Items']

    if not len(items):
        return

    for item in items:
        key_dict = {k: item[k] for k in keys}
        table.delete_item(Key=key_dict)


def create_init_user():
    """Create initial admin user for authentication purposes."""
    data = {
        'username': "testing_admin",
        'password': "password",
    }

    user_model.create(data, users_table)
