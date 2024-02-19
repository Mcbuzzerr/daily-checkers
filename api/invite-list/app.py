import boto3
from os import getenv
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Invites")


def lambda_handler(event, context):

    if (("pathParameters" in event)):

        path = event["pathParameters"]
        if path is None or "id" not in path:
            return response(200, table.scan()["Items"])
        
        if path is not None and "id" in path:
            id = path["id"]
            output = table.get_item(Key={"id": id})["Item"]
            return response(200, output)

    return response(200, table.scan()["Items"])


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }
