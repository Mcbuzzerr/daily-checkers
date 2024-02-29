import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
from datetime import datetime

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("")
user_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users"
)
sqs = boto3.client("sqs", region_name=region_name)


def lambda_handler(event, context):
    # path = event["pathParameters"]
    # id = path["id"]
    pass


def send_game_end_notification(winner, loser):
    winner = user_table.get_item(Key={"id": winner["id"]})["Item"]
    loser = user_table.get_item(Key={"id": loser["id"]})["Item"]

    if winner["victories"] == 0:
        winner_message = f"Congratulations, {winner['name']}! You just won a game of checkers against {loser['name']}! With this victory, you have unlocked the ability to customize your pieces and profile! Go to the settings page to check it out!"
    else:
        winner_message = f"Congratulations, {winner['name']}! You just won a game of checkers against {loser['name']}! You now have {winner['victories']} victories!"

    sqs.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/385155794368/my-queue",
        MessageBody=notification(
            winner["email"],
            winner["name"],
            "You got that W in a game of checkers!",
            winner_message,
        ),
    )

    sqs.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/385155794368/my-queue",
        MessageBody=notification(
            loser["email"],
            loser["name"],
            "You just suffered from a skill issue in checkers...",
            f"Sorry, {loser['name']}. You just lost a game of checkers against {winner['name']}. Better luck next time!",
        ),
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
