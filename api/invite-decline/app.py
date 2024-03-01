import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import pymysql.cursors
import json

region_name = getenv("APP_REGION")
table = pymysql.connect(
    host="dailycheckers-mysql.cpeg0mmogxkq.us-east-1.rds.amazonaws.com",
    user="trumpetbeast",
    password="2JDfC1YtMiKLa17cdscj",
    database="dailycheckers_invites",
    cursorclass=pymysql.cursors.DictCursor,
)


def lambda_handler(event, context):
    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    id = event["pathParameters"]["id"]
    invite_decliner = authenticated_user["id"]

    with table:
        with table.cursor() as cursor:
            cursor = table.cursor()
            cursor.execute(f"SELECT * FROM invites WHERE id = '{id}'")
            invite = cursor.fetchone()

            if not invite:
                return response(404, {"error": "Invite not found"})
            else:
                if invite["to"] != invite_decliner:
                    return response(403, {"error": "Unauthorized"})

                cursor.execute(f"DELETE FROM invites WHERE id = '{id}'")
                table.commit()

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
