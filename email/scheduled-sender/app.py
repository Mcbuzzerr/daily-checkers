import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
from datetime import datetime, timedelta
import time
import platform
import smtplib
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid
from pydantic import BaseModel


class Message(BaseModel):
    subject: str
    recipient_email: str
    recipient_name: str
    email_text: str


class Notification(BaseModel):
    id: str
    message: Message
    status: str
    send_at: str


region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("NotificationTable")

smtp_config = {
    "host": getenv("SMTP_HOST"),
    "port": getenv("SMTP_PORT"),
    "username": getenv("SMTP_USERNAME"),
    "password": getenv("SMTP_PASSWORD"),
    "name": getenv("SMTP_NAME"),
}


def lambda_handler(event, context):
    results = table.scan(
        FilterExpression=Attr("status").eq("pending")
        & Attr("send_at").lt(datetime.now().isoformat())
    )
    for item in results["Items"]:
        print(item)
        # Data models subject to change, as they don't exist yet
        with smtplib.SMTP(smtp_config["host"], smtp_config["port"]) as server:
            server.starttls()
            server.login(smtp_config["username"], smtp_config["password"])
            server.send_message(
                build_email(
                    item["message"]["subject"],
                    item["message"]["recipient_email"],
                    item["message"]["recipient_name"],
                    item["message"]["email_text"],
                    item["message"]["email_html"],
                )
            )
            item["status"] = "sent"
            # Copilot snipper vvv --- Test me before use
            table.update_item(
                Key={"id": item["id"]},
                UpdateExpression="set #s = :s",
                ExpressionAttributeNames={"#s": "status"},
                ExpressionAttributeValues={":s": item["status"]},
            )
    return response(200, {"message": "Emails sent successfully"})


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
