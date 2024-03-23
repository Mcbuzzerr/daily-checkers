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
    invite_decliner = authenticated_user["id"]

    table_response = table.scan(
        FilterExpression=Attr("id").eq(id) & Attr("from").eq(invite_decliner)
    )

    if table_response["Count"] == 0:
        return response(404, {"error": "Invite not found"})
    else:
        invite = table_response["Items"][0]
        if invite["from"] != invite_decliner:
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
