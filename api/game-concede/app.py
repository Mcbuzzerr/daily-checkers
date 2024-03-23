import boto3
from decimal import Decimal
from os import getenv
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Games_SAM_dev"
)
user_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users_SAM_dev"
)


def lambda_handler(event, context):
    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    id = event["pathParameters"]["id"]
    game = table.get_item(Key={"id": id})

    if "Item" not in game:
        return response(404, {"error": "Game not found"})
    else:
        game = game["Item"]
        if game["players"]["A"]["id"] == authenticated_user["id"]:
            user = user_table.get_item(Key={"id": game["players"]["B"]["id"]})["Item"]
        else:
            user = user_table.get_item(Key={"id": game["players"]["A"]["id"]})["Item"]

        game["gameOver"] = True
        game["winner"] = user["id"]

        table.put_item(Item=game)

        return response(200, {"message": "Game deleted"})


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
