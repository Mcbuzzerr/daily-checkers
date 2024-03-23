import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
from datetime import datetime
from decimal import Decimal

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Games_SAM_dev"
)
user_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users_SAM_dev"
)


def lambda_handler(event, context):

    path = event["pathParameters"]
    if "id" not in path:
        return response(200, table.scan()["Items"])

    id = path["id"]
    game = table.get_item(Key={"id": id})

    if "Item" not in game:
        return response(404, {"error": "Game not found"})
    else:
        user_ids = []
        for player in game["Item"]["players"]:
            user_ids.append(game["Item"]["players"][player]["id"])

        users = user_table.scan(FilterExpression=Attr("id").is_in(user_ids))

        for player in game["Item"]["players"]:
            for user in users["Items"]:
                if user["id"] == game["Item"]["players"][player]["id"]:
                    if "password" in user:
                        del user["password"]
                    game["Item"]["players"][player]["account"] = user

        return response(200, game["Item"])


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
