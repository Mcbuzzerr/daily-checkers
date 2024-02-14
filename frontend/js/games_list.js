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
            "id": "123123-123123-123123-123213", //Invite Code
            "from": "213123-123123-123123-123213",
            "from-name": "Player A",
            "from-background-color": "#adadad",
            "from-highlight-color": "#ffe600",
            "to": "213123-123123-123123-123213",
        },
        {
            "id": "123123-123123-123123-123213", //Invite Code
            "from": "213123-123123-123123-123213",
            "from-name": "Player A",
            "from-background-color": "#adadad",
            "from-highlight-color": "#ffe600",
            "to": "213123-123123-123123-123213",
        },
        {
            "id": "123123-123123-123123-123213", //Invite Code
            "from": "213123-123123-123123-123213",
            "from-name": "Player A",
            "from-background-color": "#adadad",
            "from-highlight-color": "#ffe600",
            "to": "213123-123123-123123-123213",
        },
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
                You have no game invites at this time.
            </h3>
        </div>`;
        document.getElementById('game-container').appendChild(inviteElement);
    }
};

const playGameClicked = (gameId) => {
    // window.location.href = `/play_game#game=${gameId}`;
    console.log(gameId)
}

window.onload = async () => {
    getGameList();
};