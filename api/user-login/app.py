import boto3
from boto3.dynamodb.conditions import Attr
import os
import json
import jwt
from datetime import datetime, timedelta
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


dynamodb = boto3.resource("dynamodb", region_name=os.getenv("APP_REGION"))
table = dynamodb.Table("DailyCheckers_Users")


def lambda_handler(event, context):
    body = json.loads(event["body"])
    email = body["email"]
    password = body["password"]

    response = table.scan(FilterExpression=Attr("email").eq(email))

    # Be wary of this line
    user = response["Items"][0]
    print(user)

    if "Items" not in response or not (user["password"] == password):
        return format_response(401, {"message": "Authentication failed"})

    token = generate_jwt(email)
    user.pop("password")

    return format_response(200, {"token": token, "user": user})


def generate_jwt(email):
    payload = {"email": email, "exp": datetime.utcnow() + timedelta(days=2)}
    # Generate private key with: openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
    private_key_env_var = os.getenv("PRIVATE_KEY")
    private_key = private_key_env_var.replace("\\n", "\n")
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token


def format_response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, cls=DecimalEncoder),
        "isBase64Encoded": False,
    }
