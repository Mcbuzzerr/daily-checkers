import boto3
from os import getenv
from uuid import uuid4
import json
import pymysql.cursors

region_name = getenv("APP_REGION")
user_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users"
)
sqs = boto3.client("sqs", region_name=region_name)


def lambda_handler(event, context):
    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    invite_id = str(uuid4())
    invite_to = event["pathParameters"]["id"]
    invite_from = authenticated_user["id"]
    invite_from_name = authenticated_user["name"]
    invite_from_background = authenticated_user["backgroundColor"]
    invite_from_highlight = authenticated_user["highlightColor"]

    if invite_to == "random":
        # Look for another invite with no recipient
        # If found, use that invite's id
        # If not found, create a new invite
        pass

    # Validate invite_to id and retrieve name if valid
    recipient = user_table.get_item(Key={"id": invite_to})
    if "Item" not in recipient:
        return response(404, {"error": "Recipient not found"})
    else:
        invite_to_name = recipient["Item"]["name"]

    with pymysql.connect(
        host="dailycheckers-mysql.cpeg0mmogxkq.us-east-1.rds.amazonaws.com",
        user="trumpetbeast",
        password="2JDfC1YtMiKLa17cdscj",
        database="dailycheckers_invites",
        cursorclass=pymysql.cursors.DictCursor,
    ) as table:
        with table.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO invites (`id`, `from`, `from-name`, `from-background-color`, `from-highlight-color`, `to`, `to-name`) VALUES ('{invite_id}', '{invite_from}', '{invite_from_name}', '{invite_from_background}', '{invite_from_highlight}', '{invite_to}', '{invite_to_name}')"
            )
        table.commit()

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
