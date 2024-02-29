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
let loggedInPlayer = null;


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
    let piece_player = Object.keys(piece)[0].split("-")[1];

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



            } else if (Object.keys(Game.board[y_check][x_check])[0].split("-")[1] !== piece_player) {
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
    let pieceText = Players[Object.keys(piece)[0].split("-")[1]].pieces[Object.keys(piece)[0]].displayText;
    new_cell.innerHTML = `<div class="piece ghost ${piece.promoted ? "promoted" : ""}" id="${Object.keys(piece)[0]}">${pieceText}</div>`
    old_cell.innerHTML = `<div class="piece shadow ${piece.promoted ? "promoted" : ""}" id="shadow"></div>`;
    clearSelection();
    clearHighlights();
}

const undo = () => {
    location.reload();
}

const getGame = async (gameId) => {
    let url = `https://hjpe29d12e.execute-api.us-east-1.amazonaws.com/1/game/view/${gameId}`;
    let gameData = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then((response) => {
        return response.json();
    }).then((data) => {
        return data;
    });
    console.log(gameData);
    return gameData;
};

const setColors = (players) => {
    let root = document.documentElement;
    root.style.setProperty("--player-a-piece-color-primary", players.A.piecesAColor);
    root.style.setProperty("--player-b-piece-color-primary", players.B.piecesBColor);
}

const renderPlayers = () => {
    let playerA = document.getElementById("player-a-slate");
    let playerB = document.getElementById("player-b-slate");
    playerA.style.backgroundColor = Players.A.account.backgroundColor;
    playerA.querySelector(".playerName").innerHTML = Players.A.account.name;
    playerA.querySelector(".friendCode").innerHTML = Players.A.account.id;
    playerA.querySelector(".player-victories").innerHTML = Players.A.account.victories;
    playerB.style.backgroundColor = Players.B.account.backgroundColor;
    playerB.querySelector(".friendCode").innerHTML = Players.B.account.id;
    playerB.querySelector(".playerName").innerHTML = Players.B.account.name;
    playerB.querySelector(".player-victories").innerHTML = Players.B.account.victories;
    document.documentElement.setAttribute("player-a-outline-color", Players.A.account.highlightColor);
    document.documentElement.setAttribute("player-b-outline-color", Players.B.account.highlightColor);
    playerA.addEventListener("click", () => {
        let areTheySure = confirm(`Leave this game and view ${Players.A.account.name}'s profile?`);
        if (areTheySure) {
            window.location.href = `profile.html?user=${Players.A.account.id}`;
        }
    });
    playerB.addEventListener("click", () => {
        let areTheySure = confirm(`Leave this game and view ${Players.B.account.name}'s profile?`);
        if (areTheySure) {
            window.location.href = `profile.html?user=${Players.B.account.id}`;
        }
    });
}


window.onload = async () => {
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const game_id = urlParams.get('game');
    console.log(game_id);

    Game = await getGame(game_id);
    loggedInPlayer = await getUser();

    if (loggedInPlayer == null) {
        alert("You are not logged in");
        window.location.href = "index.html";
    }

    Players.A = Game.players.A
    Players.B = Game.players.B
    console.log(Players);

    renderPlayers();

    // Get Game from backend instead of this ^^^^
    setColors(Players);
    renderBoard(Game);
    document.addEventListener("dblclick", () => {
        clearSelection();
        clearHighlights();
    })
}