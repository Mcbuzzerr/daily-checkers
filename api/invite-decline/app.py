import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Invites_SAM"
)


def lambda_handler(event, context):
    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    id = event["pathParameters"]["id"]
    invite_decliner = event["invite_decliner"]

    response = table.scan(
        KeyConditionExpression=Key("id").eq(id),
        FilterExpression=Attr("to").eq(invite_decliner),
    )

    if response["Count"] == 0:
        return response(404, {"error": "Invite not found"})
    else:
        invite = response["Items"][0]
        if invite["to"] != invite_decliner:
            return response(403, {"error": "Unauthorized"})

        table.delete_item(Key={"id": id})
        return response(200, {"message": "Invite declined"})


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
