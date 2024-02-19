import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
from datetime import datetime

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Games")


def lambda_handler(event, context):
    id = event["id"]
    game = table.get_item(Key={"id": id})

    if game is None:
        return response(404, {"error": "Game not found"})
    else:
        game["deleted"] = True
        game["board"] = None
        table.put_item(Item=game)
        return response(200, game)


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }
