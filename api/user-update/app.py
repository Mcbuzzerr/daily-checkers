import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
from datetime import datetime
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Users")


def lambda_handler(event, context):

    id = event["pathParameters"]["id"]
    body = json.loads(event["body"])
    name = None
    email = None
    password = None
    highlight_color = None

    if "name" in body:
        name = body["name"]
    if "email" in body:
        email = body["email"]
    if "password" in body:
        password = body["password"]
    if "highlight-color" in body:
        highlight_color = body["highlight-color"]

    user = table.get_item(Key={"id": id})["Item"]

    if user is None:
        return response(404, {"error": "User not found"})
    else:
        if name is not None:
            user["name"] = name
        if email is not None:
            user["email"] = email
        if password is not None:
            user["password"] = password
        if highlight_color is not None:
            user["highlight-color"] = highlight_color
        print(user)
        table.put_item(Item=user)
        return response(200, user)


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, cls=DecimalEncoder),
        "isBase64Encoded": False,
    }
