import boto3
from decimal import Decimal
from os import getenv
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Users")


def lambda_handler(event, context):

    id = event["pathParameters"]["id"]
    body = json.loads(event["body"])
    name = None
    email = None
    password = None

    if "name" in body:
        name = body["name"]
    if "email" in body:
        email = body["email"]
    if "password" in body:
        password = body["password"]

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


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o)
        return super(DecimalEncoder, self).default(o)
