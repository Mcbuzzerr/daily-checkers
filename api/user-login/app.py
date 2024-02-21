import boto3
from boto3.dynamodb.conditions import Attr
import os
import json
import jwt
from datetime import datetime, timedelta
import hashlib
import binascii

dynamodb = boto3.resource("dynamodb", region_name=os.getenv("APP_REGION"))
table = dynamodb.Table("DailyCheckers_Users")


def login_handler(event, context):
    body = json.loads(event["body"])
    email = body["email"]
    password = body["password"]

    response = table.scan(FilterExpression=Attr("email").eq(email))

    # Be wary of this line
    user = (
        response["Items"][0]
        if "Items" in response and len(response["Items"]) > 0
        else None
    )

    if "Item" not in response or not (user["password"] == password):
        return format_response(401, {"message": "Authentication failed"})

    token = generate_jwt(email)
    user.pop("password")

    return format_response(200, {"token": token, "user": user})


def generate_jwt(email):
    payload = {"email": email, "exp": datetime.utcnow() + timedelta(days=2)}
    # Generate private key with: openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
    private_key = os.getenv("PRIVATE_KEY")
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token


def format_response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }
