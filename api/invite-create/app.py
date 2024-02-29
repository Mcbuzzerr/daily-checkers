import boto3
from os import getenv
from uuid import uuid4
import json

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Invites"
)
sqs = boto3.client("sqs", region_name=region_name)


def lambda_handler(event, context):

    invite_id = str(uuid4())
    invite_from = event["from"]
    invite_from_name = event["from-name"]
    invite_from_background = event["from-background-color"]
    invite_from_highlight = event["from-highlight-color"]
    invite_to = event["to"]

    invite = {
        "id": invite_id,
        "from": invite_from,
        "from-name": invite_from_name,
        "from-background-color": invite_from_background,
        "from-highlight-color": invite_from_highlight,
        "to": invite_to,
    }

    table.put_item(Item=invite)

    URL = "localhost:5500"

    sqs.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/385155794368/my-queue",
        MessageBody=notification(
            invite_to,
            "Daily Checkers User",
            "You've been invited to play a match of Checkers",
            f"You've been invited (Dare I say Challenged?) to play Checkers by {invite_from_name}. Click here to view your pending invites: https://{URL}/invites",
        ),
    )

    return response(200, invite)


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
