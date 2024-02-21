import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
import jwt

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Users")


def lambda_handler(event, context):
    auth_token = event["authorizationToken"].split(" ")[1]

    # generate private key with:
    # openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
    # then extract public key with:
    # openssl rsa -pubout -in private_key.pem -out public_key.pem

    public_key = getenv("PUBLIC_KEY")

    decoded_token = jwt.decode(auth_token, public_key, algorithms=["RS256"])

    user_or_false = found_in_db(decoded_token)

    if user_or_false:
        allow = "Allow"

    response = {
        "principalId": f"{decoded_token['email']}",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": allow,
                    "Resource": event["methodArn"],
                }
            ],
        },
        "context": {
            "user": user_or_false,
        },
    }

    return response


def found_in_db(decoded_token):
    print(decoded_token)
    email = decoded_token["email"]
    user = table.scan(FilterExpression=Attr("email").eq(email))

    if len(user["Items"]) == 1:
        return user["Items"][0]
    else:
        return False


def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
        "isBase64Encoded": False,
    }
