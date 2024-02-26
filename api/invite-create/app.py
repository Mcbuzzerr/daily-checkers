import boto3
from os import getenv
from uuid import uuid4
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Invites"
)


def lambda_handler(event, context):

    invite_id = str(uuid4())
    invite_from = event["from"]
    invite_from_name = event["from-name"]
    invite_from_background = event["from-background-color"]
    invite_from_highlight = event["from-highlight-color"]
    invite_to = event["to"]

    invite = {
        "id": invite_id,
        "from": invite_from,
        "from-name": invite_from_name,
        "from-background-color": invite_from_background,
        "from-highlight-color": invite_from_highlight,
        "to": invite_to,
    }

    table.put_item(Item=invite)
    return response(200, invite)


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
