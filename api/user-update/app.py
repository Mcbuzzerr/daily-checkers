import boto3
from decimal import Decimal
from os import getenv
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Users")


def lambda_handler(event, context):

    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    id = event["pathParameters"]["id"]

    if authenticated_user["id"] != id:
        return response(403, {"error": "Forbidden"})

    body = json.loads(event["body"])

    if "confirmPassword" not in body:
        return response(400, {"error": "Confirm password is required"})

    if "name" in body:
        name = body["name"]
    if "email" in body:
        email = body["email"]
    if "password" in body:
        password = body["password"]

    user = table.get_item(Key={"id": id})["Item"]

    if body["confirmPassword"] != user["password"]:
        return response(400, {"error": "Password confirmation failed"})

    if user is None:
        return response(404, {"error": "User not found"})
    else:
        if name is not None:
            user["name"] = name
        if email is not None:
            user["email"] = email
        if password is not None:
            user["password"] = password
        print(user)
        table.put_item(Item=user)
        return response(200, user)


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
