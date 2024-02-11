const alphabetArray = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
let showCoords = false;
let gameBoard = null;
let selected_piece = null;
let pieceMoved = false;
let Game = null;


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
            let pieceText = game.players[game_board[y][x].id.split("-")[1]].pieces[game_board[y][x].id.split("-")[0] - 1].displayText;
            let color = game_board[y][x].id.split("-")[1] === "A" ? "black" : "white";
            cells[i].innerHTML = `<div class="piece ${color}" id="${game_board[y][x].id}">${pieceText}</div>`;
            if (game.turnCount % 2 === 0 && game_board[y][x].id.split("-")[1] === "A" || game.turnCount % 2 !== 0 && game_board[y][x].id.split("-")[1] === "B") {
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

const setColors = (players) => {
    let root = document.documentElement;
    root.style.setProperty("--player-a-piece-color-primary", players.A.primaryColor);
    root.style.setProperty("--player-b-piece-color-primary", players.B.primaryColor);
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
    console.log("Highlighting moves");
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
                    console.log("Moving piece");
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
                            console.log("Moving piece");
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
    pieceMoved = true;
    if (selected_piece == null) return;

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

window.onload = () => {


    Game = {
        players: {
            A: {
                pieces: ["OwO", "UwU", "EwE", "Salo", "Fridge", "🐈", "🦈", "0 - 0", ">w>", "Squij", "🐛", "Pheeb"],
                primaryColor: "black",
                secondaryColor: "white",
            },
            B: {
                pieces: ["^_^", "(•_•)", "O.O", "^o^", "X_X", "ᓚᘏᗢ", "💀", "🐢", "/ᐠ｡ꞈ｡ᐟ\\", "Sheem", "Pinto", ":3"],
                primaryColor: "white",
                secondaryColor: "black",
            },
        },
        turnCount: 0,
        board: [
            [
                null,
                {
                    id: "1-A",
                    promoted: false,
                },
                null,
                {
                    id: "2-A",
                    promoted: false,
                },
                null,
                {
                    id: "3-A",
                    promoted: false,
                },
                null,
                {
                    id: "4-A",
                    promoted: false,
                },
            ],
            [
                {
                    id: "5-A",
                    promoted: false,
                },
                null,
                {
                    id: "6-A",
                    promoted: false,
                },
                null,
                {
                    id: "7-A",
                    promoted: false,
                },
                null,
                {
                    id: "8-A",
                    promoted: false,
                },
            ],
            [
                null,
                {
                    id: "9-A",
                    promoted: false,
                },
                null,
                {
                    id: "10-A",
                    promoted: false,
                },
                null,
                {
                    id: "11-A",
                    promoted: false,
                },
                null,
                {
                    id: "12-A",
                    promoted: false,
                },
            ],
            [
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
            ],
            [
                null,
                null,
                null,
                null,
                null,
                null,
                null,
                null,
            ],
            [
                {
                    id: "1-B",
                    promoted: false,
                },
                null,
                {
                    id: "2-B",
                    promoted: false,
                },
                null,
                {
                    id: "3-B",
                    promoted: false,
                },
                null,
                {
                    id: "4-B",
                    promoted: false,
                },
            ],
            [
                null,
                {
                    id: "5-B",
                    promoted: false,
                },
                null,
                {
                    id: "6-B",
                    promoted: false,
                },
                null,
                {
                    id: "7-B",
                    promoted: false,
                },
                null,
                {
                    id: "8-B",
                    promoted: false,
                },
            ],
            [
                {
                    id: "9-B",
                    promoted: false,
                },
                null,
                {
                    id: "10-B",
                    promoted: false,
                },
                null,
                {
                    id: "11-B",
                    promoted: false,
                },
                null,
                {
                    id: "12-B",
                    promoted: false,
                },
            ]
        ]
    };

    // Get Game from backend instead of this ^^^^

    setColors(Game.players);
    renderBoard(Game);
    document.addEventListener("dblclick", () => {
        console.log("Clearing selections");
        clearSelection();
        clearHighlights();
    })
}