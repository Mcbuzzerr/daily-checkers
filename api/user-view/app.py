import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
from decimal import Decimal
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Users")

def lambda_handler(event, context):    
    path = event["pathParameters"]
    if "id" not in path:
        return response(200, table.scan()["Items"])
    
    id = path["id"]

    user = table.get_item(Key={"id": id})

    if user is None:
        return response(404, {"error": "User not found"})
    else:
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