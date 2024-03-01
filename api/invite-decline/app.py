import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import mysql.connector
import json

region_name = getenv("APP_REGION")
table = mysql.connector.connect(
    host="dailycheckers-mysql.cpeg0mmogxkq.us-east-1.rds.amazonaws.com",
    user="trumpetbeast",
    password="2JDfC1YtMiKLa17cdscj",
    database="dailycheckers_invites",
)

def lambda_handler(event, context):
    id = event["pathParameters"]["id"]
    invite_decliner = event["invite_decliner"]

    cursor = table.cursor()
    cursor.execute(f"SELECT * FROM invites WHERE id = '{id}'")
    invites = cursor.fetchone()

    if not invites:
        return response(404, {"error": "Invite not found"})
    else:
        invite = {
            "id": invites[0],
            "from": invites[1],
            "from-name": invites[2],
            "from-background-color": invites[3],
            "from-highlight-color": invites[4],
            "to": invites[5],
            "to-name": invites[6],
        }
        if invite["to"] != invite_decliner:
            return response(403, {"error": "Unauthorized"})

        cursor.execute(f"DELETE FROM invites WHERE id = '{id}'")
        table.commit()
        cursor.close()

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
