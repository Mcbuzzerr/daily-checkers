import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
from datetime import datetime

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table("DailyCheckers_Games")
user_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users"
)
notification_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Notifications_SAM"
)
sqs = boto3.client("sqs", region_name=region_name)


def lambda_handler(event, context):
    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    new_game_state = json.loads(event["body"])
    game_id = new_game_state["id"]
    print(new_game_state)
    print(game_id)
    game = table.get_item(Key={"id": game_id})
    user_a = user_table.get_item(Key={"id": game["Item"]["players"]["A"]["id"]})["Item"]
    user_b = user_table.get_item(Key={"id": game["Item"]["players"]["B"]["id"]})["Item"]

    if "Item" not in game:
        return response(404, {"error": "Game not found."})

    old_game_state = game["Item"]

    # check if it's the authenticated user's turn

    authenticated_user_team = (
        "A" if old_game_state["players"]["A"]["id"] == authenticated_user["id"] else "B"
    )

    # if old_game_state["turnCount"] % 2 == 0:
    #     if authenticated_user_team != "A":
    #         return response(400, {"error": "It's not your turn."})
    # elif old_game_state["turnCount"] % 2 == 1:
    #     if authenticated_user_team != "B":
    #         return response(400, {"error": "It's not your turn."})

    # check which pieces are alive

    old_board = old_game_state["board"]
    new_board = new_game_state["board"]

    previously_alive_pieces = []
    currently_alive_pieces = []

    for row in old_board:
        for cell in row:
            if cell != None:
                for key in cell:
                    previously_alive_pieces.append(
                        {
                            "key": key,
                            "position": f"{old_board.index(row)}-{row.index(cell)}",
                        }
                    )

    for row in new_board:
        for cell in row:
            if cell != None:
                for key in cell:
                    currently_alive_pieces.append(
                        {
                            "key": key,
                            "position": f"{new_board.index(row)}-{row.index(cell)}",
                        }
                    )

    for piece in previously_alive_pieces:
        if piece["key"] not in currently_alive_pieces:
            piece_team = piece["key"].split("-")[1]
            if piece_team == "A":
                user_a["pieces"][piece["key"]]["lifetimeDeaths"] += 1
            elif piece_team == "B":
                user_b["pieces"][piece["key"]]["lifetimeDeaths"] += 1

    print("Checking for movement")
    for piece in currently_alive_pieces:
        for piece_b in previously_alive_pieces:
            if piece_b["key"] == piece["key"]:
                print(piece)
                print(piece_b)
                print(piece["position"])
                print(piece_b["position"])

    # Check for promotions
    # untested copilot code 😎
    if authenticated_user_team == "A":
        for cell in new_board[0]:
            if cell != None:
                for key in cell:
                    if "A" in key:
                        new_board[0][new_board[0].index(cell)] = {key: True}
    elif authenticated_user_team == "B":
        for cell in new_board[7]:
            if cell != None:
                for key in cell:
                    if "B" in key:
                        new_board[7][new_board[7].index(cell)] = {key: True}
    # untested copilot code 😎

    return response(
        200,
        {
            "previously_alive_pieces": previously_alive_pieces,
            "currently_alive_pieces": currently_alive_pieces,
        },
    )

    # check if the game is over

    # update the game state

    new_game_state["turnCount"] += 1
    new_game_state["players"][authenticated_user_team][
        "lastTurnTakenAt"
    ] = datetime.now().isoformat()

    table.put_item(Item=new_game_state)

    # send a notification to the other player

    return response(200, {"message": "Game state updated."})


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
