import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
from datetime import datetime

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Users")


def lambda_handler(event, context):
   
    id = event["id"]
    name = None
    email = None
    password = None
    background_color = None
    highlight_color = None

    if "name" in event:
        name = event["name"]
    if "email" in event:
        email = event["email"]
    if "password" in event:
        password = event["password"]
    if "background-color" in event:
        background_color = event["background-color"]
    if "highlight-color" in event:
        highlight_color = event["highlight-color"]

    user = table.get_item(Key={"id": id})

    if user is None:
        return response(404, {"error": "User not found"})
    else:
        if name is not None:
            user["name"] = name
        if email is not None:
            user["email"] = email
        if password is not None:
            user["password"] = password
        if background_color is not None:
            user["background-color"] = background_color
        if highlight_color is not None:
            user["highlight-color"] = highlight_color
        table.put_item(Item=user)
        return response(200, user)

def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }
