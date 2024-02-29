import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
from datetime import datetime
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("")

smtp_config = {
    "host": getenv("SMTP_HOST"),
    "port": getenv("SMTP_PORT"),
    "username": getenv("SMTP_USERNAME"),
    "password": getenv("SMTP_PASSWORD"),
    "name": getenv("SMTP_NAME"),
}


def lambda_handler(event, context):
    print(event)
    message = json.loads(event["Records"][0]["body"])

    with smtplib.SMTP(smtp_config["host"], smtp_config["port"]) as server:
        server.starttls()
        server.login(smtp_config["username"], smtp_config["password"])
        server.send_message(
            build_email(
                message["subject"],
                message["recipient_email"],
                message["recipient_name"],
                message["email_text"],
            )
        )

    return response(200, "Email sent")


def build_email(subject_line, recipient_email, recipient_name, email_text):
    email_message = EmailMessage()

    email_message["Subject"] = subject_line
    email_message["From"] = Address(
        smtp_config["name"],
        smtp_config["username"].split("@")[0],
        smtp_config["username"].split("@")[1],
    )

    email_message["To"] = Address(
        recipient_name,
        recipient_email.split("@")[0],
        recipient_email.split("@")[1],
    )

    text_content = email_text
    email_message.set_content(text_content)

    return email_message


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
