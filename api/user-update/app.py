import boto3
import hashlib
from decimal import Decimal
from os import getenv
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Users")
sqs = boto3.client("sqs", region_name=region_name)


def lambda_handler(event, context):

    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    id = event["pathParameters"]["id"]

    if authenticated_user["id"] != id:
        return response(403, {"error": "Forbidden"})

    body = json.loads(event["body"])

    if "confirmPassword" not in body:
        return response(400, {"error": "Confirm password is required"})

    if "name" in body:
        name = body["name"]
    if "email" in body:
        email = body["email"]
    if "password" in body:
        password = hash256(str(body["password"]))

    user = table.get_item(Key={"id": id})["Item"]

    if hash256(str(body["confirmPassword"])) != user["password"]:
        return response(400, {"error": "Password confirmation failed"})

    if user is None:
        return response(404, {"error": "User not found"})
    else:
        if name is not None:
            user["name"] = name
        if email is not None:
            user["email"] = email
        if password is not None:
            user["password"] = password
        table.put_item(Item=user)

        sqs.send_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/385155794368/my-queue",
            MessageBody=notification(
                authenticated_user["email"],
                authenticated_user["name"],
                "Your account has been updated",
                "Someone has successfully updated your account, hopefully it was you! Chances are it was because who would want to hack a checkers account?",
            ),
        )

        return response(200, user)
    

def hash256(obj):
    return hashlib.sha256(obj.encode()).hexdigest()


def notification(recipient_email, recipient_name, subject, contents):
    return json.dumps(
        {
            "recipient_email": recipient_email,
            "recipient_name": recipient_name,
            "subject": subject,
            "email_text": contents,
        }
    )


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


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o)
        return super(DecimalEncoder, self).default(o)
