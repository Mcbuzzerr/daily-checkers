import boto3
from os import getenv
import json
from uuid import uuid4

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Users")


def lambda_handler(event, context):
    
    user_id = uuid4()
    user_name = event["name"]
    user_email = event["email"]
    user_password = event["password"]
    user_victories = 0

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
    return response(200, user)



def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }
