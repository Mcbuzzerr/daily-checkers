import boto3
from decimal import Decimal
from os import getenv
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Games")


def lambda_handler(event, context):
    id = event["id"]
    game = table.get_item(Key={"id": id})

    if game is None:
        return response(404, {"error": "Game not found"})
    else:
        game = game["Item"]
        game["deleted"] = True
        game["board"] = None
        table.put_item(Item=game)
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
        "body": json.dumps(body, cls=DecimalEncoder),
        "isBase64Encoded": False,
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o)
        return super(DecimalEncoder, self).default(o)
