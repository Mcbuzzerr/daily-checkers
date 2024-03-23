import boto3
from boto3.dynamodb.conditions import Attr
from os import getenv
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Invites_SAM_dev"
)


def lambda_handler(event, context):
    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    id = authenticated_user["id"]

    invites_to = table.scan(FilterExpression=Attr("to").eq(id))

    invites_from = table.scan(FilterExpression=Attr("from").eq(id))

    if invites_to["Count"] == 0 and invites_from["Count"] == 0:
        return response(200, {"message": "No invites found"})
    else:
        return response(
            200,
            {"invitesTo": invites_to["Items"], "invitesFrom": invites_from["Items"]},
        )


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
