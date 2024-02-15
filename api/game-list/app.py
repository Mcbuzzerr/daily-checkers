import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
from datetime import datetime

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("")


def lambda_handler(event, context):
    # path = event["pathParameters"]
    # id = path["id"]

    # a game in Json looks like this:
    # {
    #     "players": {
    #         "A": {
    #             "id": "213123-123123-123123-123213",
    #             "lastTurnTakenAt": "TIMESTAMP"
    #         },
    #         "B": {
    #             "id": "213123-123123-123123-123213",
    #             "lastTurnTakenAt": "TIMESTAMP"
    #         }
    #     },
    #     "turnCount": 0,
    #     "board": 2DArray[][] # Sudocode for brevity
    # };

    # To avoid the frontend needing to make multiple requests
    # to get the game list and then the user profiles, I think
    # it would be best to return the user's name with the game

    # {
    #     "players": {
    #         "A": {
    #             "id": "213123-123123-123123-123213",
    #             "name": "John Doe",
    #             "lastTurnTakenAt": "TIMESTAMP"
    #         },
    #         "B": {
    #             "id": "213123-123123-123123-123213",
    #             "name": "Jane Doe",
    #             "lastTurnTakenAt": "TIMESTAMP"
    #         }
    #     },
    #     "turnCount": 0,
    #     "board": 2DArray[][] # Sudocode for brevity
    # };
    pass


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }
