import boto3
from boto3.dynamodb.conditions import Key
from os import getenv
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users_SAM"
)
sqs = boto3.client("sqs", region_name=region_name)


def lambda_handler(event, context):

    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    id = event["pathParameters"]["id"]
    if authenticated_user["id"] != id:
        return response(403, {"error": "Forbidden"})

    users = table.query(
        KeyConditionExpression=Key("id").eq(id),
    )

    if users["Count"] == 0:
        return response(404, {"error": "User not found"})
    else:
        user = users["Items"][0]
        table.delete_item(Key={"id": user["id"]})

        sqs.send_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/385155794368/my-queue",
            MessageBody=notification(
                authenticated_user["email"],
                authenticated_user["name"],
                "Your account has been deleted",
                "Someone has successfully deleted your account, hopefully it was you! It was probably you, because why would someone else want to delete your account? A juicy rivalry? Anyways, if this was a mistake let us know and we can try to pull some necromancy on your account!",
            ),
        )

        return response(200, {"message": "User deleted"})


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


def notification(recipient_email, recipient_name, subject, contents):
    return json.dumps(
        {
            "recipient_email": recipient_email,
            "recipient_name": recipient_name,
            "subject": subject,
            "email_text": contents,
        }
    )
