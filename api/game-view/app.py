import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
from datetime import datetime

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Games")


def lambda_handler(event, context):

    path = event["pathParameters"]
    if "id" not in path:
        return response(200, table.scan()["Items"])

    id = path["id"]
    game = table.get_item(Key={"id": id})

    if game is None:
        return response(404, {"error": "Game not found"})
    else:
        return response(200, game)


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
