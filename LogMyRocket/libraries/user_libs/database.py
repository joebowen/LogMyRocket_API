import sys, os
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "../sys_packages"))

import boto3


db = boto3.resource('dynamodb', region_name='us-east-1')

if 'TESTING' in os.environ:
    users_table = db.Table('LogMyRocketUsersTest')
    rockets_table = db.Table('LogMyRocketRocketsTest')
    flights_table = db.Table('LogMyRocketFlightsTest')
else:
    users_table = db.Table('LogMyRocketUsers')
    rockets_table = db.Table('LogMyRocketRockets')
    flights_table = db.Table('LogMyRocketFlights')