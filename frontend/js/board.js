const alphabetArray = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
let showCoords = false;
let gameBoard = null;
let selected_piece = null;
let pieceMoved = false;
let Game = null;
let Players = {
    "A": null,
    "B": null
}


const renderBoard = (
    game
) => {
    // Iterate through cells attaching IDs and placing pieces
    let cells = document.querySelectorAll(".cell");

    let x = 0;
    let y = 0;
    let game_board = game.board;

    for (let i = 0; i < cells.length; i++) {


        x = i % 8;
        y = Math.floor(i / 8);
        cells[i].id = `${x}-${y}`;

        if (game_board[y][x] != null) {
            cells[i].innerHTML = game_board[y][x].id;
            let piece_id = Object.keys(game_board[y][x])[0];
            let pieceText = Players[piece_id.split("-")[1]].pieces[piece_id].displayText;
            let color = piece_id.split("-")[1] === "A" ? "black" : "white";
            cells[i].innerHTML = `<div class="piece ${color}" id="${piece_id}">${pieceText}</div>`;
            if (game.turnCount % 2 === 0 && piece_id.split("-")[1] === "A" || game.turnCount % 2 !== 0 && piece_id.split("-")[1] === "B") {
                cells[i].addEventListener("click", selectPiece);
            }
        } else {
            cells[i].innerHTML = "";
        }

        if (showCoords) {
            cells[i].innerHTML = cells[i].innerHTML + `${x}-${y}`;
        }
    }
}

const selectPiece = (event) => {
    clearHighlights();
    clearSelection();
    let piece = event.target;
    let cell = event.target.parentElement;
    let x = cell.id.split("-")[0];
    let y = cell.id.split("-")[1];
    selected_piece = Game.board[y][x];
    if (selected_piece != null) {
        highlightMoves(x, y);
        piece.classList.add("selected");
    }
}

const highlightMoves = (x, y) => {
    let piece = selected_piece;
    let piece_player = piece.id.split("-")[1];

    for (let i = -1; i <= 1; i += 2) {
        let x_check = parseInt(x) + i;
        let y_check = parseInt(y) + (piece_player === "A" ? 1 : -1);
        if (x_check >= 0 && x_check <= 7 && y_check >= 0 && y_check <= 7) {
            if (Game.board[y_check][x_check] === null) {
                let cell = document.getElementById(`${x_check}-${y_check}`);
                cell.classList.add("highlighted");
                cell.addEventListener("click", () => {
                    planMovePiece(piece, x, y, x_check, y_check);
                });



            } else if (Game.board[y_check][x_check].id.split("-")[1] !== piece_player) {
                let x_jump = x_check + i;
                let y_jump = y_check + (piece_player === "A" ? 1 : -1);
                if (x_jump >= 0 && x_jump <= 7 && y_jump >= 0 && y_jump <= 7) {
                    if (Game.board[y_jump][x_jump] === null) {
                        let cell = document.getElementById(`${x_jump}-${y_jump}`);
                        cell.classList.add("highlighted");
                        cell.addEventListener("click", () => {
                            planMovePiece(piece, x, y, x_jump, y_jump);
                        });
                    }
                }
            }
        }
    }
}

const clearSelection = () => {
    document.querySelectorAll(".selected").forEach((el) => {
        el.classList.remove("selected");
    });
    selected_piece = null;
}

const clearHighlights = () => {
    document.querySelectorAll(".highlighted").forEach((el) => {
        el.classList.remove("highlighted");
    });
}

const planMovePiece = (piece, old_x, old_y, new_x, new_y) => {
    if (pieceMoved) {
        return;
    }
    if (selected_piece == null) return;
    pieceMoved = true;
    let undoButton = document.getElementById("undo-button");
    undoButton.classList.remove("disabled");
    let submitButton = document.getElementById("submit-button");
    submitButton.classList.remove("disabled");

    let old_cell = document.getElementById(`${old_x}-${old_y}`);
    let new_cell = document.getElementById(`${new_x}-${new_y}`);
    let pieceText = Game.players[piece.id.split("-")[1]].pieces[piece.id.split("-")[0] - 1];
    new_cell.innerHTML = `<div class="piece ghost ${piece.promoted ? "promoted" : ""}" id="${piece.id}">${pieceText}</div>`
    old_cell.innerHTML = `<div class="piece shadow ${piece.promoted ? "promoted" : ""}" id="shadow"></div>`;
    clearSelection();
    clearHighlights();
}

const undo = () => {
    location.reload();
}

const getGame = async (gameId) => {
    return {
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
};

const getPlayer = async (playerId) => {
    return {
        "id": playerId, //Friend Code
        "name": "Player A",
        "email": "playerA@email.com",
        "password": "shhhhhhhhhhhhh",
        "victories": 1,
        "pieces": {
            "1-A": { // {PieceNumber}-{TeamLetter} A = Black, B = Whit: {

                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0, //Display ratio on stats page
                "lifetimePromotions": 0
            },
            "2-A": {

                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "3-A": {

                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "4-A": {

                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "5-A": {

                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "6-A": {

                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "7-A": {

                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "8-A": {

                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "9-A": {

                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "10-A": {

                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "11-A": {

                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "12-A": {

                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "1-B": {
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "2-B": {
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "3-B": {
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "4-B": {
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "5-B": {
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "6-B": {
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "7-B": {
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "8-B": {
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "9-B": {
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "10-B": {
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "11-B": {
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            "12-B": {
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            }
        },
        "piecesAColor": "#000000",
        "piecesBColor": "#ffffff",
        "highlightColor": "#ffe600",
        "backgroundColor": "#adadad"
    }
};


const setColors = (players) => {
    let root = document.documentElement;
    root.style.setProperty("--player-a-piece-color-primary", players.A.piecesAColor);
    root.style.setProperty("--player-b-piece-color-primary", players.B.piecesBColor);
}

window.onload = async () => {


    Game = await getGame("asdasd");
    Players = {
        "A": await getPlayer(Game.players.A.id),
        "B": await getPlayer(Game.players.B.id)
    }


    // Get Game from backend instead of this ^^^^
    setColors(Players);
    renderBoard(Game);
    document.addEventListener("dblclick", () => {
        clearSelection();
        clearHighlights();
    })
}