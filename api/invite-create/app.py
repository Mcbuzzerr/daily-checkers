import boto3
from os import getenv
from uuid import uuid4
import json
import pymysql.cursors

region_name = getenv("APP_REGION")
user_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users_SAM"
)
game_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Games_SAM"
)


def lambda_handler(event, context):
    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    invite_id = str(uuid4())
    invite_to = event["pathParameters"]["id"]
    invite_from = authenticated_user["id"]
    invite_from_name = authenticated_user["name"]
    invite_from_background = authenticated_user["backgroundColor"]
    invite_from_highlight = authenticated_user["highlightColor"]
    URL = "localhost:5500/frontend"

    if invite_to == invite_from:
        return response(400, {"error": "You cannot invite yourself to a game"})

    with pymysql.connect(
        host="dailycheckers-mysql.cpeg0mmogxkq.us-east-1.rds.amazonaws.com",
        user="trumpetbeast",
        password="2JDfC1YtMiKLa17cdscj",
        database="dailycheckers_invites",
        cursorclass=pymysql.cursors.DictCursor,
    ) as table:
        with table.cursor() as cursor:
            if invite_to == "random":
                # Look for another invite with no recipient
                cursor.execute(
                    "SELECT * FROM invites WHERE `to` IS NULL ORDER BY RAND() LIMIT 1"
                )
                result = cursor.fetchone()
                if result:
                    invite_to = result["from"]

                    opponent = user_table.get_item(Key={"id": invite_to})["Item"]

                    if opponent["id"] == invite_from:
                        return response(
                            400, {"message": "You cannot invite yourself to a game"}
                        )

                    game = {
                        "id": str(uuid4()),
                        "players": {
                            "A": {
                                "id": authenticated_user["id"],
                                "lastTurnTakenAt": None,
                            },
                            "B": {"id": opponent["id"], "lastTurnTakenAt": None},
                        },
                        "turnCount": 0,
                        "gameOver": False,
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

                    cursor.execute(f"DELETE FROM invites WHERE `id` = '{result['id']}'")
                    table.commit()
                    return response(200, {"gameID": game["id"]})

                else:
                    # If not found, create a new invite
                    cursor.execute(
                        f"INSERT INTO invites (`id`, `from`, `from-name`, `from-background-color`, `from-highlight-color`) VALUES ('{invite_id}', '{invite_from}', '{invite_from_name}', '{invite_from_background}', '{invite_from_highlight}')"
                    )
                    table.commit()
                    return response(
                        200,
                        {"message": "Game will be created when an opponent is found"},
                    )

            # Validate invite_to id and retrieve name if valid
            recipient = user_table.get_item(Key={"id": invite_to})
            if "Item" not in recipient:
                return response(404, {"message": "Recipient not found"})
            else:
                invite_to_name = recipient["Item"]["name"]

                cursor.execute(
                    f"INSERT INTO invites (`id`, `from`, `from-name`, `from-background-color`, `from-highlight-color`, `to`, `to-name`) VALUES ('{invite_id}', '{invite_from}', '{invite_from_name}', '{invite_from_background}', '{invite_from_highlight}', '{invite_to}', '{invite_to_name}')"
                )
                table.commit()

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
