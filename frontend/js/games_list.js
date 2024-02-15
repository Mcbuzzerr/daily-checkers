let loggedInUser = null;
// Fetch Invites
// Generate Invite List
// Accept Invites
// Decline Invites
// Send Invites

const getGameList = async () => {
    let gameList = [];
    // fetch('/api/invite/list', {
    //     method: 'GET',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    // }).then((response) => {
    //     return response.json();
    // }).then((data) => {
    //     console.log(data);
    //     inviteList = data;
    // });
    gameList = [
        {
            "players": {
                "A": {
                    "id": "213123-123123-123123-123213",
                    "name": "Player 1",
                    "lastTurnTakenAt": "TIMESTAMP"
                },
                "B": {
                    "id": "213123-123123-123123-123213",
                    "name": "Player 2",
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
        },
        {
            "players": {
                "A": {
                    "id": "113123-123123-123123-123213",
                    "name": "Player 1",
                    "lastTurnTakenAt": "TIMESTAMP"
                },
                "B": {
                    "id": "213123-123123-123123-123213",
                    "name": "Player 2",
                    "lastTurnTakenAt": "TIMESTAMP"
                }
            },
            "turnCount": 1,
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
        }
    ];

    for (let i = 0; i < gameList.length; i++) {
        let game = gameList[i];
        let inviteElement = document.createElement('div');
        inviteElement.classList.add('slate');
        inviteElement.classList.add('game');
        let turn = game.turnCount % 2 === 1 ? "White" : "Black";
        let totalWhite = 0;
        let totalBlack = 0;

        for (let iter = 0; iter < game.board.length; iter++) {
            let row = game.board[iter];
            for (let j = 0; j < row.length; j++) {
                let cell = row[j];
                if (cell !== null) {
                    if (Object.keys(cell)[0].split("-")[1] == "A") {
                        totalBlack++;
                    } else {
                        totalWhite++;
                    }
                }
            }
        }


        let header3Text = null;
        // Check if the invite is from the current user
        // Change the invite text if so
        // Display Game data such as turn number, current turn, etc.
        if (game.players.A.id === loggedInUser.id) {
            header3Text = `You have invited <span class="player-name bold">${game.players.B["name"]}</span> to play a game of checkers.`;
        } else {
            header3Text = `<span class="player-name bold">${game.players.A["name"]}</span> has invited you to play a game of checkers.`;
        }


        inviteElement.innerHTML = `
            <h3>
                ${header3Text}
            </h3>
            <div class="button-container">
                <p class="button submit" onclick="playGameClicked('${game.id}')">View Game</p>
                <h3 class="no-margin">Current Turn: <span style="color: ${turn};">${turn}</span></h3>
                <h3 class="no-margin">
                    <span style="color: black;">${totalBlack}</span> vs. <span style="color: white;">${totalWhite}</span>
                </h1>
                <p class="button cancel" onclick="handleConcedeClicked()">Concede</p>
            </div>`; // turncount % 2 = 1 or 0, 0 is black or white idk yet

        document.getElementById('game-container').appendChild(inviteElement);
    }

    if (gameList.length === 0) {
        let inviteElement = document.createElement('div');
        // inviteElement.classList.add('slate');
        // inviteElement.classList.add('invite');
        inviteElement.innerHTML = `
        <div id="no-invites-message" class="slate hidden">
            <h3>
                You have no games    at this time.
            </h3>
        </div>`;
        document.getElementById('game-container').appendChild(inviteElement);
    }
};

const playGameClicked = (gameId) => {
    window.location.href = `/frontend/play_game.html?game=${gameId}`;
    console.log(gameId)
};

const handleConcedeClicked = () => {
    let areTheySure = confirm("Are you sure you want to concede the game?");
    alert(areTheySure)
}

window.onload = async () => {
    loggedInUser = await getUser();
    getGameList();
};