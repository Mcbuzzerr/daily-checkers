import boto3
from os import getenv
import json
import hashlib
from uuid import uuid4
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users_SAM"
)


def lambda_handler(event, context):
    print(event)
    user_id = uuid4()
    body = json.loads(event["body"])
    user_name = body["name"]
    user_email = body["email"]
    user_password = hash256(str(body["password"]))
    user_victories = 0

    user_with_email = table.scan(FilterExpression=Attr("email").eq(user_email))

    if user_with_email["Items"]:
        return response(400, {"error": "Email already in use"})

    blankPiece = {
        "displayText": "",
        "lifetimeKills": 0,
        "lifetimeDeaths": 0,
        "lifetimePromotions": 0,
    }
    user_pieces = {
        "1-A": blankPiece,
        "2-A": blankPiece,
        "3-A": blankPiece,
        "4-A": blankPiece,
        "5-A": blankPiece,
        "6-A": blankPiece,
        "7-A": blankPiece,
        "8-A": blankPiece,
        "9-A": blankPiece,
        "10-A": blankPiece,
        "11-A": blankPiece,
        "12-A": blankPiece,
        "1-B": blankPiece,
        "2-B": blankPiece,
        "3-B": blankPiece,
        "4-B": blankPiece,
        "5-B": blankPiece,
        "6-B": blankPiece,
        "7-B": blankPiece,
        "8-B": blankPiece,
        "9-B": blankPiece,
        "10-B": blankPiece,
        "11-B": blankPiece,
        "12-B": blankPiece,
    }

    user_piecesAColor = "#000000"
    user_piecesBColor = "#ffffff"
    user_highlightColor = "#ffe600"
    user_backgroundColor = "#adadad"

    user = {
        "id": str(user_id),
        "name": user_name,
        "email": user_email,
        "password": user_password,
        "victories": user_victories,
        "pieces": user_pieces,
        "piecesAColor": user_piecesAColor,
        "piecesBColor": user_piecesBColor,
        "highlightColor": user_highlightColor,
        "backgroundColor": user_backgroundColor,
    }

    table.put_item(Item=user)

    return response(200, {"message": "User created successfully"})


def hash256(obj):
    return hashlib.sha256(obj.encode()).hexdigest()


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
