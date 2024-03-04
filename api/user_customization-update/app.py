import boto3
from os import getenv
import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o)
        return super(DecimalEncoder, self).default(o)


region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users_SAM"
)


def lambda_handler(event, context):
    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    id = event["pathParameters"]["id"]
    if authenticated_user["id"] != id:
        return response(403, {"error": "Forbidden"})

    body = json.loads(event["body"])
    pieces = None
    highlight_color = None
    background_color = None
    pieces_a_color = None
    pieces_b_color = None

    if "pieces" in body:
        pieces = body["pieces"]
    if "highlightColor" in body:
        highlight_color = body["highlightColor"]
    if "backgroundColor" in body:
        background_color = body["backgroundColor"]
    if "piecesAColor" in body:
        pieces_a_color = body["piecesAColor"]
    if "piecesBColor" in body:
        pieces_b_color = body["piecesBColor"]

    user = table.get_item(Key={"id": id})

    if "Item" not in user:
        return response(404, {"error": "User not found"})
    else:
        user = user["Item"]
        if pieces is not None:
            user["pieces"] = pieces
        if highlight_color is not None:
            user["highlightColor"] = highlight_color
        if background_color is not None:
            user["backgroundColor"] = background_color
        if pieces_a_color is not None:
            user["piecesAColor"] = pieces_a_color
        if pieces_b_color is not None:
            user["piecesBColor"] = pieces_b_color
        table.put_item(Item=user)
        del user["password"]
        return response(200, user)


def response(code, body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        },
        "body": json.dumps(body, cls=DecimalEncoder),
        "isBase64Encoded": False,
    }
