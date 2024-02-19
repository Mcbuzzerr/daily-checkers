import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
from datetime import datetime

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCHeckers_Users")

def lambda_handler(event, context):
    id = event["id"]
    pieces = event["pieces"]

    user = table.get_item(Key={"id": id})

    if user is None:
        return response(404, {"error": "User not found"})
    
    user["pieces"] = pieces
    table.put_item(Item=user)
    return response(200, user)

def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }
