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
        }
    ];

    for (let i = 0; i < gameList.length; i++) {
        let invite = gameList[i];
        let inviteElement = document.createElement('div');
        inviteElement.classList.add('slate');
        inviteElement.classList.add('game');
        inviteElement.style.backgroundColor = invite["from-background-color"];

        // Check if the invite is from the current user
        // Change the invite text if so
        // Display Game data such as turn number, current turn, etc.
        inviteElement.innerHTML = `
        <h3>
            <span class="player-name bold" style="color: ${invite["from-highlight-color"]};">${invite["from-name"]}</span> has invited you to play a game of checkers.
        </h3>
        <div class="button-container">
            <p class="button submit" onclick="playGameClicked('${invite.id}')">Play Game</p>
        </div>`;

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
}

window.onload = async () => {
    getGameList();
};