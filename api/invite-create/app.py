import boto3
from os import getenv
from uuid import uuid4
import json
import mysql.connector

region_name = getenv("APP_REGION")
user_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users"
)
table = mysql.connector.connect(
    host="dailycheckers-mysql.cpeg0mmogxkq.us-east-1.rds.amazonaws.com",
    user="trumpetbeast",
    password="2JDfC1YtMiKLa17cdscj",
    database="dailycheckers_invites",
)
sqs = boto3.client("sqs", region_name=region_name)


def lambda_handler(event, context):

    invite_id = str(uuid4())
    invite_from = event["from"]
    invite_from_name = event["from-name"]
    invite_from_background = event["from-background-color"]
    invite_from_highlight = event["from-highlight-color"]
    invite_to = event["to"]
    invite_to_name = None

    # Validate invite_to id and retrieve name if valid
    recipient = user_table.get_item(Key={"id": invite_to})
    if "Item" not in recipient:
        return response(404, {"error": "Recipient not found"})
    else:
        invite_to_name = recipient["Item"]["name"]

    # Insert invite into database
    cursor = table.cursor()
    cursor.execute(
        f"INSERT INTO invites (`id`, `from`, `from-name`, `from-background-color`, `from-highlight-color`, `to`, `to-name`) VALUES ('{invite_id}', '{invite_from}', '{invite_from_name}', '{invite_from_background}', '{invite_from_highlight}', '{invite_to}', '{invite_to_name}')"
    )
    table.commit()
    cursor.close()

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

    return response(200, {"inviteID": invite_id})


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
