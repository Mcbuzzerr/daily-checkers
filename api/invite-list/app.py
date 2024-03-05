import boto3
from boto3.dynamodb.conditions import Attr
from os import getenv
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Invites_SAM"
)


def lambda_handler(event, context):
    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    id = authenticated_user["id"]

    if "pathParameters" in event:

        invites = table.scan(FilterExpression=Attr("to").eq(id))

        if invites["Count"] == 0:
            return response(200, {"message": "No invites found"})
        else:
            return response(200, invites["Items"])

    return response(200, table.scan()["Items"])


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
