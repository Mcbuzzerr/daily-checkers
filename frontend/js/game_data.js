// Doesn't include "promoted" property because that's a game state thing
let Piece_inDB = {
    "id": "1-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
    "displayText": "text",
    "lifetimeKills": 0,
    "lifetimeDeaths": 0, //Display ratio on stats page
    "lifetimePromotions": 0
}

let PlayerA_inDB = {
    "id": "213123-123123-123123-123213", //Friend Code
    "name": "Player A",
    "email": "playerA@email.com",
    "password": "shhhhhhhhhhhhh",
    "victories": 1,
    "pieces": [
        Piece_inDB, // List of pieces includes black and white
    ],
    "piecesAColor": "#000000",
    "piecesBColor": "#ffffff",
    "highlightColor": "#ffe600",
    "backgroundColor": "#adadad"
}

let Piece_inGame = {
    "1-A": false // {PieceNumber}-{TeamLetter} A = Black, B = White
}

let Game_inDB = {
    "players": {
        "A": {
            "id": "213123-123123-123123-123213",
            "lastTurnTakenAt": "TIMESTAMP"
        },
        "B": {
            "id": "213123-123123-123123-123213",
            "lastTurnTakenAt": "TIMESTAMP"
        }
    },
    "turnCount": 0,
    "board": [
        [
            null,
            {
                "1-A": false
            },
            null,
            {
                "2-A": false
            },
            null,
            {
                "3-A": false
            },
            null,
            {
                "4-A": false
            }
        ],
        [
            {
                "5-A": false
            },
            null,
            {
                "6-A": false
            },
            null,
            {
                "7-A": false
            },
            null,
            {
                "8-A": false
            }
        ],
        [
            null,
            {
                "9-A": false
            },
            null,
            {
                "10-A": false
            },
            null,
            {
                "11-A": false
            },
            null,
            {
                "12-A": false
            }
        ],
        [
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
        ],
        [
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            null
        ],
        [
            {
                "1-B": false
            },
            null,
            {
                "2-B": false
            },
            null,
            {
                "3-B": false
            },
            null,
            {
                "4-B": false
            }
        ],
        [
            null,
            {
                "5-B": false
            },
            null,
            {
                "6-B": false
            },
            null,
            {
                "7-B": false
            },
            null,
            {
                "8-B": false
            }
        ],
        [
            {
                "9-B": false
            },
            null,
            {
                "10-B": false
            },
            null,
            {
                "11-B": false
            },
            null,
            {
                "12-B": false
            }
        ]
    ]
};

let invite_inDB = {
    "id": "123123-123123-123123-123213", //Invite Code
    "from": "213123-123123-123123-123213",
    "from-name": "Player A",
    "from-background-color": "#adadad",
    "from-highlight-color": "#ffe600",
    "to": "213123-123123-123123-123213",
}