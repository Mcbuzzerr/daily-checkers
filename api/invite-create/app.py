import boto3
from os import getenv
from uuid import uuid4
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import json
import random

region_name = getenv("APP_REGION")
user_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users_SAM"
)
game_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Games_SAM"
)
invite_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Invites_SAM"
)


def lambda_handler(event, context):
    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    invite_id = str(uuid4())
    invite_to = event["pathParameters"]["id"]
    invite_from = authenticated_user["id"]
    invite_from_name = authenticated_user["username"]
    invite_from_background = authenticated_user["backgroundColor"]
    invite_from_highlight = authenticated_user["highlightColor"]
    URL = "localhost:5500/frontend"

    if invite_to == invite_from:
        return response(400, {"error": "You cannot invite yourself to a game"})

    if invite_to == "random":
        # Look for another invite with no recipient
        random_invites = invite_table.scan(
            FilterExpression=Attr("to").eq(None) & Attr("from").ne(invite_from)
        )

        if random_invites["Count"] > 0:
            random_index = random.randint(0, random_invites["Count"] - 1)
            invite = random_invites["Items"][random_index]

            if invite["from"] == invite_from:
                return response(400, {"error": "You cannot invite yourself to a game"})

            # Check that the account is still active
            recipient = user_table.get_item(Key={"id": invite["from"]})
            if "Item" not in recipient:
                return response(404, {"error": "Recipient not found"})

            game = {
                "id": str(uuid4()),
                "players": {
                    "A": {
                        "id": authenticated_user["id"],
                        "lastTurnTakenAt": None,
                    },
                    "B": {"id": invite["from"], "lastTurnTakenAt": None},
                },
                "turnCount": 0,
                "gameOver": False,
                "winner": None,
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

            # Remove the invite from the table
            invite_table.delete_item(Key={"id": invite["id"]})

            return response(200, {"gameID": game["id"]})

        else:
            invites_from_user = invite_table.scan(
                FilterExpression=Attr("to").eq(None) & Attr("from").eq(invite_from)
            )

            if invites_from_user["Count"] > 0:
                return response(
                    200,
                    {"message": "Game will be created when an opponent is found"},
                )

            # If not found, create a new invite
            invite_table.put_item(
                Item={
                    "id": invite_id,
                    "from": invite_from,
                    "from-name": invite_from_name,
                    "from-background-color": invite_from_background,
                    "from-highlight-color": invite_from_highlight,
                    "to": None,
                    "to-name": "Random",
                }
            )
            return response(
                200,
                {"message": "Game will be created when an opponent is found"},
            )

    # Validate invite_to id and retrieve name if valid
    recipient = user_table.get_item(Key={"id": invite_to})
    if "Item" not in recipient:
        return response(404, {"error": "Recipient not found"})
    else:
        invite_to_name = recipient["Item"]["username"]

        # Create the invite
        invite_table.put_item(
            Item={
                "id": invite_id,
                "from": invite_from,
                "from-name": invite_from_name,
                "from-background-color": invite_from_background,
                "from-highlight-color": invite_from_highlight,
                "to": invite_to,
                "to-name": invite_to_name,
            }
        )

        return response(200, {"inviteID": invite_id})


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
