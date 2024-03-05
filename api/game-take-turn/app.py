import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
from os import getenv
import json
from datetime import datetime, timedelta
from uuid import uuid4

region_name = getenv("APP_REGION")
table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Games_SAM"
)
user_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Users_SAM"
)
notification_table = boto3.resource("dynamodb", region_name=region_name).Table(
    "DailyCheckers_Notifications_SAM"
)
sqs = boto3.client("sqs", region_name=region_name)


def lambda_handler(event, context):
    authenticated_user = json.loads(event["requestContext"]["authorizer"]["user"])
    new_game_state = json.loads(event["body"])
    game_id = new_game_state["id"]
    game = table.get_item(Key={"id": game_id})
    user_a = user_table.get_item(Key={"id": game["Item"]["players"]["A"]["id"]})["Item"]
    user_b = user_table.get_item(Key={"id": game["Item"]["players"]["B"]["id"]})["Item"]

    if "Item" not in game:
        return response(404, {"error": "Game not found."})

    old_game_state = game["Item"]

    if old_game_state["gameOver"]:
        return response(400, {"error": "The game is over."})

    if new_game_state["turnCount"] != old_game_state["turnCount"]:
        return response(400, {"error": "Invalid turn count."})

    # check if it's the authenticated user's turn

    authenticated_user_team = (
        "A" if old_game_state["players"]["A"]["id"] == authenticated_user["id"] else "B"
    )

    # if old_game_state["players"][authenticated_user_team]["lastTurnTakenAt"] != None:
    #     last_turn_taken_at = datetime.fromisoformat(
    #         old_game_state["players"][authenticated_user_team]["lastTurnTakenAt"]
    #     )
    #     print((datetime.now() - last_turn_taken_at))
    #     if (datetime.now() - last_turn_taken_at).days < 1:
    #         return response(400, {"error": "You can only take one turn every 24 hours"})

    if old_game_state["turnCount"] % 2 == 0:
        if authenticated_user_team != "A":
            return response(400, {"error": "It's not your turn."})
    elif old_game_state["turnCount"] % 2 == 1:
        if authenticated_user_team != "B":
            return response(400, {"error": "It's not your turn."})

    new_game_state["players"][authenticated_user_team][
        "lastTurnTakenAt"
    ] = datetime.now().isoformat()
    new_game_state["turnCount"] += 1
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

    currently_alive_team_a_pieces = []
    currently_alive_team_b_pieces = []

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
                    if "A" in key:
                        currently_alive_team_a_pieces.append(key)
                    elif "B" in key:
                        currently_alive_team_b_pieces.append(key)
    piecesKilled = 0

    print(previously_alive_pieces)
    print(currently_alive_pieces)
    for old_piece in previously_alive_pieces:
        isPieceStillAlive = False
        print("Checking if piece is still alive")
        print(old_piece)
        for new_piece in currently_alive_pieces:
            print(new_piece)
            if old_piece["key"] == new_piece["key"]:
                isPieceStillAlive = True
                print("Piece is still alive")
                break
        if not isPieceStillAlive:
            print("Piece is dead")
            print(old_piece["key"])
            if "A" in old_piece["key"]:
                user_a["pieces"][old_piece["key"]]["lifetimeDeaths"] += 1
                piecesKilled += 1
                print("Lifetime deaths added to ", old_piece["key"])
                print(user_a["pieces"][old_piece["key"]])
            elif "B" in old_piece["key"]:
                user_b["pieces"][old_piece["key"]]["lifetimeDeaths"] += 1
                piecesKilled += 1
                print("Lifetime deaths added to ", old_piece["key"])
                print(user_b["pieces"][old_piece["key"]])

    print(piecesKilled)
    if piecesKilled > 0:
        for piece_prev in previously_alive_pieces:
            for piece_curr in currently_alive_pieces:
                if piece_prev["key"] == piece_curr["key"]:
                    if piece_prev["position"] != piece_curr["position"]:
                        if "A" in piece_prev["key"]:
                            user_a["pieces"][piece_prev["key"]][
                                "lifetimeKills"
                            ] += piecesKilled
                            print("Lifetime kills added to ", piece_prev["key"])
                            print(user_a["pieces"][piece_prev["key"]])
                        elif "B" in piece_prev["key"]:
                            user_b["pieces"][piece_prev["key"]][
                                "lifetimeKills"
                            ] += piecesKilled
                            print("Lifetime kills added to ", piece_prev["key"])
                            print(user_b["pieces"][piece_prev["key"]])

    # Check for promotions
    if authenticated_user_team == "A":
        for cell in new_board[7]:
            if cell != None:
                for key in cell:
                    if "A" in key:
                        print("I deserve a promotion! - ", key)
                        new_board[7][new_board[7].index(cell)] = {key: True}
                        user_a["pieces"][key]["lifetimePromotions"] += 1
    elif authenticated_user_team == "B":
        for cell in new_board[0]:
            if cell != None:
                for key in cell:
                    if "B" in key:
                        print("I deserve a promotion! - ", key)
                        new_board[0][new_board[0].index(cell)] = {key: True}
                        user_b["pieces"][key]["lifetimePromotions"] += 1

    # check if the game is over
    if len(currently_alive_team_a_pieces) == 0:
        # team B wins
        user_b["victories"] += 1
        new_game_state["gameOver"] = True
        send_game_end_notification(user_b, user_a)
        table.put_item(Item=new_game_state)
        user_table.put_item(Item=user_a)
        user_table.put_item(Item=user_b)
        return response(200, {"message": "Game over. Team B wins."})
    elif len(currently_alive_team_b_pieces) == 0:
        # team A wins
        user_a["victories"] += 1
        new_game_state["gameOver"] = True
        send_game_end_notification(user_a, user_b)
        table.put_item(Item=new_game_state)
        user_table.put_item(Item=user_a)
        user_table.put_item(Item=user_b)
        return response(200, {"message": "Game over. Team A wins."})

    send_at_24_hours_from_now = datetime.now() + timedelta(hours=24)

    notification_table.put_item(
        Item=scheduled_notification(
            send_at_24_hours_from_now.isoformat(),
            authenticated_user["email"],
            authenticated_user["name"],
            "Your next turn is ready!",
            "It's your turn again in your game of checkers!",
        )
    )

    opponent = user_a if authenticated_user_team == "B" else user_b

    sqs.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/385155794368/my-queue",
        MessageBody=notification(
            opponent["email"],
            opponent["name"],
            "Your opponent has taken their turn",
            "Your opponent has taken their turn in your game of checkers!",
        ),
    )

    # update the user stats
    user_table.put_item(Item=user_a)
    user_table.put_item(Item=user_b)
    # update the game state
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


def add_text_to_winner_pieces(winner):
    winner_pieces = winner["pieces"]
    winner_pieces[0]["displyText"] = "Click"
    winner_pieces[1]["displyText"] = "Piece"
    winner_pieces[2]["displyText"] = "To"
    winner_pieces[3]["displyText"] = "Customize"
    winner_pieces[4]["displyText"] = "Your"
    winner_pieces[5]["displyText"] = "Pieces"
    winner_pieces[6]["displyText"] = "Names"
    winner_pieces[7]["displyText"] = "And"
    winner_pieces[8]["displyText"] = "Hover"
    winner_pieces[9]["displyText"] = "Over"
    winner_pieces[10]["displyText"] = "Them"
    winner_pieces[11]["displyText"] = "To"
    winner_pieces[12]["displyText"] = "See"
    winner_pieces[13]["displyText"] = "Their"
    winner_pieces[14]["displyText"] = "Stats"


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


def scheduled_notification(send_at, recipient_email, recipient_name, subject, contents):
    return {
        "id": str(uuid4()),
        "send_at": send_at,
        "recipient_email": recipient_email,
        "recipient_name": recipient_name,
        "subject": subject,
        "email_text": contents,
    }
