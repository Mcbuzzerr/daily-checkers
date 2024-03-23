import boto3
import hashlib
from decimal import Decimal
from os import getenv
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users_SAM_dev"
)


def lambda_handler(event, context):

    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    id = event["pathParameters"]["id"]

    if authenticated_user["id"] != id:
        return response(403, {"error": "Forbidden"})

    body = json.loads(event["body"])
    username = None
    newPassword = None

    if "confirmPassword" not in body:
        return response(400, {"error": "Confirm password is required"})

    if "username" in body:
        username = body["username"]
    if "newPassword" in body:
        newPassword = hash256(str(body["newPassword"]))

    user = table.get_item(Key={"id": id})["Item"]

    if hash256(str(body["confirmPassword"])) != user["password"]:
        return response(400, {"error": "Password confirmation failed"})

    if user is None:
        return response(404, {"error": "User not found"})
    else:
        if username is not None:
            user["username"] = username
        if newPassword is not None:
            user["password"] = newPassword
        table.put_item(Item=user)

        del user["password"]

        return response(200, user)


def hash256(obj):
    return hashlib.sha256(obj.encode()).hexdigest()


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
