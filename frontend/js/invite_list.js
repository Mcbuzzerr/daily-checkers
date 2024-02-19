// Fetch Invites
// Generate Invite List
// Accept Invites
// Decline Invites
// Send Invites

const getInviteList = async () => {
    let inviteList = [];
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
    inviteList = [
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

    for (let i = 0; i < inviteList.length; i++) {
        let invite = inviteList[i];
        let inviteElement = document.createElement('div');
        inviteElement.classList.add('slate');
        inviteElement.classList.add('invite');
        inviteElement.style.backgroundColor = invite["from-background-color"];
        inviteElement.innerHTML = `
        <h3>
            <span class="player-name bold" style="color: ${invite["from-highlight-color"]};">${invite["from-name"]}</span> has invited you to play a game of checkers.
        </h3>
        <div class="button-container">
            <p class="button submit" onclick="acceptInviteClicked('${invite.id}')">Accept</p>
            <p class="button cancel" onclick="declineInviteClicked('${invite.id}')">Decline</p>
        </div>
            `;

        document.getElementById('invite-container').appendChild(inviteElement);
    }

    if (inviteList.length === 0) {
        let inviteElement = document.createElement('div');
        // inviteElement.classList.add('slate');
        // inviteElement.classList.add('invite');
        inviteElement.innerHTML = `
        <div id="no-invites-message" class="slate hidden">
            <h3>
                You have no game invites at this time.
            </h3>
        </div>
            `;
        document.getElementById('invite-container').appendChild(inviteElement);
    }
};

const acceptInviteClicked = async (inviteId) => {
    console.log(inviteId);
    alert(`Invite ${inviteId} accepted`);
};

const declineInviteClicked = async (inviteId) => {
    console.log(inviteId);
    alert(`Invite ${inviteId} declined`);
};

const handleNewInviteClicked = () => {
    let friendCode = document.getElementById('friend-code').value;
    if (friendCode) {
        alert('Invite sent to friend code: ' + friendCode);
    } else {
        alert('Please enter a friend code');
    }
};


window.onload = async () => {
    getInviteList();
};