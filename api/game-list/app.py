import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from decimal import Decimal
from os import getenv
import json
from datetime import datetime

region_name = getenv("APP_REGION")
game_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Games"
)
user_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users"
)


def lambda_handler(event, context):

    path = event["pathParameters"]
    if "id" not in path:
        return response(200, game_table.scan()["Items"])

    id = path["id"]
    games = game_table.scan(
        FilterExpression=Attr("players.A.id").eq(id) | Attr("players.B.id").eq(id)
    )

    if games["Count"] == 0:
        return response(200, {"body": "No games found"})
    else:
        user_ids = []
        for game in games["Items"]:
            for player in game["players"]:
                if game["players"][player]["id"] == id:
                    game["players"][player]["name"] = "self"
                else:
                    user_ids.append(game["players"][player]["id"])

        # maybe change to a dictionary or something more efficient later?
        users = user_table.scan(FilterExpression=Attr("id").is_in(user_ids))

        for game in games["Items"]:
            for player in game["players"]:
                if game["players"][player]["id"] != id:
                    for user in users["Items"]:
                        if user["id"] == game["players"][player]["id"]:
                            game["players"][player]["name"] = user["name"]

        return response(200, games["Items"])


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
        "body": json.dumps(body, cls=DecimalEncoder),
        "isBase64Encoded": False,
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o)
        return super(DecimalEncoder, self).default(o)
