// Doesn't include "promoted" property because that's a game state thing
let Piece_inDB = {
    "id": "1-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
    "displayText": "text",
    // Stupid optional shit
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
    "id": "1-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
    "promoted": false
}

let PlayerA_frontend = {
    "id": "213123-123123-123123-123213", //Friend Code
    "name": "Player A",
    "pieces": [
        Piece_inGame, // List of pieces includes only pieces for their assigned team for this game
    ],
    "piecesColor": "#000000",
    "highlightColor": "#2940ef",
    "backgroundColor": "#5079e9",
    "lastTurnTakenAt": "TIMESTAMP"
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
                "id": "1-A",
                "promoted": false
            },
            null,
            {
                "id": "2-A",
                "promoted": false
            },
            null,
            {
                "id": "3-A",
                "promoted": false
            },
            null,
            {
                "id": "4-A",
                "promoted": false
            }
        ],
        [
            {
                "id": "5-A",
                "promoted": false
            },
            null,
            {
                "id": "6-A",
                "promoted": false
            },
            null,
            {
                "id": "7-A",
                "promoted": false
            },
            null,
            {
                "id": "8-A",
                "promoted": false
            }
        ],
        [
            null,
            {
                "id": "9-A",
                "promoted": false
            },
            null,
            {
                "id": "10-A",
                "promoted": false
            },
            null,
            {
                "id": "11-A",
                "promoted": false
            },
            null,
            {
                "id": "12-A",
                "promoted": false
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
                "id": "1-B",
                "promoted": false
            },
            null,
            {
                "id": "2-B",
                "promoted": false
            },
            null,
            {
                "id": "3-B",
                "promoted": false
            },
            null,
            {
                "id": "4-B",
                "promoted": false
            }
        ],
        [
            null,
            {
                "id": "5-B",
                "promoted": false
            },
            null,
            {
                "id": "6-B",
                "promoted": false
            },
            null,
            {
                "id": "7-B",
                "promoted": false
            },
            null,
            {
                "id": "8-B",
                "promoted": false
            }
        ],
        [
            {
                "id": "9-B",
                "promoted": false
            },
            null,
            {
                "id": "10-B",
                "promoted": false
            },
            null,
            {
                "id": "11-B",
                "promoted": false
            },
            null,
            {
                "id": "12-B",
                "promoted": false
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