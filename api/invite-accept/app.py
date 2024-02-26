import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
from uuid import uuid4
import json

region_name = getenv("APP_REGION")
invite_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Invites"
)
game_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Games"
)


def lambda_handler(event, context):
    id = event["pathParameters"]["id"]
    invite_acceptor = event["invite_acceptor"]

    invites = invite_table.get_item(Key={"id": id})
    if "Item" not in invites:
        return response(404, {"error": "Invite not found"})
    else:
        invite = invites["Item"]
        if invite["to"] != invite_acceptor:
            return response(403, {"error": "Unauthorized"})

        game = {
            "id": str(uuid4()),
            "players": {
                "A": {"id": invite["from"], "lastTurnTakenAt": None},
                "B": {"id": invite["to"], "lastTurnTakenAt": None},
            },
            "turnCount": 0,
            "board": [
                [
                    None,
                    {"1-A": False},
                    None,
                    {"2-A": False},
                    None,
                    {"3-A": False},
                    None,
                    {"4-A": False},
                ],
                [
                    {"5-A": False},
                    None,
                    {"6-A": False},
                    None,
                    {"7-A": False},
                    None,
                    {"8-A": False},
                    None,
                ],
                [
                    None,
                    {"9-A": False},
                    None,
                    {"10-A": False},
                    None,
                    {"11-A": False},
                    None,
                    {"12-A": False},
                ],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [
                    {"1-B": False},
                    None,
                    {"2-B": False},
                    None,
                    {"3-B": False},
                    None,
                    {"4-B": False},
                    None,
                ],
                [
                    None,
                    {"5-B": False},
                    None,
                    {"6-B": False},
                    None,
                    {"7-B": False},
                    None,
                    {"8-B": False},
                ],
                [
                    {"9-B": False},
                    None,
                    {"10-B": False},
                    None,
                    {"11-B": False},
                    None,
                    {"12-B": False},
                    None,
                ],
            ],
        }

        game_table.put_item(Item=game)

        invite_table.delete_item(Key={"id": invite["id"]})
        return response(200, {"gameID": game["id"]})


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }
