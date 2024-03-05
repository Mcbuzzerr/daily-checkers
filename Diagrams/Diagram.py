# diagram.py
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SimpleQueueServiceSqs as SQS
from diagrams.aws.general import User
from diagrams.custom import Custom

with Diagram("Daily-Checkers All") as diag:
    myGateway = APIGateway("API Gateway")
    myRDS = RDS("mySQL Invites DB")
    myUserDynamoDB = Dynamodb("User DynamoDB")
    myGameDynamoDB = Dynamodb("Game DynamoDB")
    myNotificationDynamoDB = Dynamodb("Notification DynamoDB")
    myNotificationQueue = SQS("Notification SQS")

    myUser = User("User")

    with Cluster("Client"):
        myHTML = Custom("HTML", "./img/html.png")
        myCSS = Custom("CSS", "./img/css.png")
        myJS = Custom("JS", "./img/javascript.png")

    with Cluster("API Gateway Lambdas"):
        with Cluster("User"):
            userRegister = Lambda("Register")
            userLogin = Lambda("Login")
            userUpdate = Lambda("Update")
            userUpdateCustomization = Lambda("Update Customization")
            userDelete = Lambda("Delete")
            userView = Lambda("View")

        with Cluster("Game"):
            gameTakeTurn = Lambda("Take Turn")
            gameConcede = Lambda("Concede")
            gameView = Lambda("View")
            gameList = Lambda("List")

        with Cluster("Invite"):
            inviteCreate = Lambda("Create")
            inviteAccept = Lambda("Accept")
            inviteDecline = Lambda("Decline")
            inviteList = Lambda("List")

    with Cluster("Authorizors"):
        userAuth = Lambda("User Auth")
        victorAuth = Lambda("Victor Auth")

    with Cluster("Notification Lambdas"):
        queuedSender = Lambda("Queued Sender")
        scheduledSender = Lambda("Scheduled Sender")

    myUser >> myHTML << Edge() >> myCSS
    myHTML << Edge() >> myJS >> myGateway
    myGateway >> userRegister >> Edge(color="purple") >> myUserDynamoDB
    myGateway >> userLogin >> Edge(color="purple") >> myUserDynamoDB
    userLogin >> Edge(color="blue") >> myNotificationQueue
    myGateway >> userAuth >> userUpdate >> Edge(color="purple") >> myUserDynamoDB
    userUpdate >> Edge(color="blue") >> myNotificationQueue
    (
        myGateway
        >> victorAuth
        >> userUpdateCustomization
        >> Edge(color="purple")
        >> myUserDynamoDB
    )
    myGateway >> userAuth >> userDelete >> Edge(color="purple") >> myUserDynamoDB
    userDelete >> Edge(color="blue") >> myNotificationQueue
    myGateway >> userAuth >> userView >> Edge(color="purple") >> myUserDynamoDB
    myGateway >> userAuth >> gameTakeTurn >> Edge(color="green") >> myGameDynamoDB
    gameTakeTurn >> Edge(color="purple") >> myUserDynamoDB
    gameTakeTurn >> Edge(color="blue") >> myNotificationQueue
    gameTakeTurn >> Edge(color="orange") >> myNotificationDynamoDB
    myGateway >> userAuth >> gameConcede >> Edge(color="green") >> myGameDynamoDB
    gameConcede >> Edge(color="purple") >> myUserDynamoDB
    gameConcede >> Edge(color="blue") >> myNotificationQueue
    myGateway >> userAuth >> gameView >> Edge(color="green") >> myGameDynamoDB
    gameView >> Edge(color="purple") >> myUserDynamoDB
    myGateway >> userAuth >> gameList >> Edge(color="green") >> myGameDynamoDB
    gameList >> Edge(color="purple") >> myUserDynamoDB
    myGateway >> userAuth >> inviteCreate >> Edge(color="red") >> myRDS
    inviteCreate >> Edge(color="purple") >> myUserDynamoDB
    inviteCreate >> Edge(color="blue") >> myNotificationQueue
    inviteCreate >> Edge(color="green") >> myGameDynamoDB
    myGateway >> userAuth >> inviteAccept >> Edge(color="red") >> myRDS
    inviteAccept >> Edge(color="blue") >> myNotificationQueue
    inviteAccept >> Edge(color="green") >> myGameDynamoDB
    myGateway >> userAuth >> inviteDecline >> Edge(color="red") >> myRDS
    myGateway >> userAuth >> inviteList >> Edge(color="red") >> myRDS
    userAuth >> Edge(color="purple") >> myUserDynamoDB
    victorAuth >> Edge(color="purple") >> myUserDynamoDB
    myNotificationQueue >> queuedSender
    myNotificationDynamoDB >> scheduledSender
