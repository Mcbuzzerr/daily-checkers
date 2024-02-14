const User = null;

const handleClickPiece = (event) => {
    // Get the piece that was clicked
    // Open up a menu allowing the user to edit the piece's text
    // (and possibly view per-piece stats)
    // ONLY AVAILABLE TO VICTORS
    console.log(event.target);
    console.log(event.target.innerHTML);
    const piece = event.target;
    const pieceText = piece.innerHTML;
    const pieceId = piece.id;
    const pieceColor = pieceId.split('-')[1] === 'A' ? 'black' : 'white';
    const textColor = pieceColor === 'black' ? 'white' : 'black';

    piece.innerHTML = `
    <input type="text" value="${pieceText}" style="width:100%; text-align: center; background-color: transparent; color: ${textColor};" />
    `;
    const label = piece.querySelector('input');
    label.focus();

    const eventListenerEvent = (event) => {
        piece.innerHTML = label.value;
        handleSavePieces();
    }

    label.addEventListener('blur', eventListenerEvent);
    label.addEventListener('keyup', (event) => {
        if (event.key === 'Enter') {
            eventListenerEvent();
        }
    });

};

const handleSavePieces = () => {
    const pieces = document.getElementsByClassName('piece');
    const pieceData = [];
    for (let piece of pieces) {
        pieceData.push({
            id: piece.id,
            displayText: piece.innerHTML,
        });
    }
    console.log(pieceData);
    // const url = 'http://localhost:3000/pieces' //Not real endpoint
    // fetch(url, {
    //     method: 'PUT',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify(pieceData),
    // })
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log('Success:', data);
    //         alert('Pieces saved successfully');
    //     })
    //     .catch((error) => {
    //         console.error('Error:', error);
    //         alert('An error occurred. Please try again later.');
    //     });
};

const handleLogoutClicked = () => {
    setCookie('user', '', 0);
    window.location.href = 'index.html'
}

const handleEditClicked = () => {
    // Show Hidden Edit Fields
    // Hide the Shown non-edit fields
    let editorSlate = document.getElementById('editor-slate');
    let playerSlate = document.getElementById('player-slate');
    editorSlate.classList.remove('hidden');
    playerSlate.classList.add('hidden');
};

const handleSaveClicked = () => {
    let playerIdElement = document.getElementById('player-id');
    let playerNameField = document.getElementById('name-field');
    let playerEmailField = document.getElementById('email-field');
    let playerNewPassword = document.getElementById('new-password-field');
    let playerConfirmPassword = document.getElementById('confirm-password-field');
    let highlightColor = document.getElementById('highlight-color');
    let backgroundColor = document.getElementById('background-color');
    let piecesAColor = document.getElementById('pieces-a-color');
    let piecesBColor = document.getElementById('pieces-b-color');
    const user = {
        id: playerIdElement.innerHTML,
        name: playerNameField.value,
        email: playerEmailField.value,
        newPassword: playerNewPassword.value,
        confirmPassword: playerConfirmPassword.value,
        highlightColor: highlightColor.value,
        backgroundColor: backgroundColor.value,
        piecesAColor: piecesAColor.value,
        piecesBColor: piecesBColor.value,
    };
    console.log(user);
    // const url = 'http://localhost:3000/profile' //Not real endpoint
    // fetch(url, {
    //     method: 'PUT',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify(user),
    // })
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log('Success:', data);
    //         renderProfile(data);
    //         setCookie('user', JSON.stringify(data), 22);
    //         handleCancelClicked();
    //     })
    //     .catch((error) => {
    //         console.error('Error:', error);
    //         alert('An error occurred. Please try again later.')
    //     });
};

const handleCancelClicked = () => {
    // Hide the editor
    // Show the player
    let editorSlate = document.getElementById('editor-slate');
    let playerSlate = document.getElementById('player-slate');
    editorSlate.classList.add('hidden');
    playerSlate.classList.remove('hidden');
};

const handleDeleteClicked = () => {
    let areTheySure = confirm('Are you sure you want to delete your account? This action cannot be undone.');
    alert(areTheySure);
};

const renderProfile = (User) => {
    let nameElement = document.getElementById('playerName');
    nameElement.innerText = User.name;
    let friendCodeElement = document.getElementById('friendCode');
    friendCodeElement.innerText = User.id;
    let playerWinsElement = document.getElementById('player-victories');
    playerWinsElement.innerText = User.victories;


    let playerPieces = User.pieces;
    let pieces = document.getElementsByClassName('piece');
    let itter_count = 0;
    for (let piece of pieces) {
        piece.innerText = playerPieces[itter_count].displayText;
        itter_count++;
    }

    // Set the colors
    document.documentElement.style.setProperty('--player-a-piece-color-primary', User.piecesAColor);
    document.documentElement.style.setProperty('--player-b-piece-color-primary', User.piecesBColor);
    document.documentElement.style.setProperty('--current-player-outline-color', User.highlightColor);
    document.documentElement.style.setProperty('--current-player-background-color', User.backgroundColor);

    // Set field values
    let playerIdElement = document.getElementById('player-id');
    playerIdElement.innerHTML = User.id;
    let playerNameField = document.getElementById('name-field');
    playerNameField.value = User.name;
    let playerEmailField = document.getElementById('email-field');
    playerEmailField.value = User.email;
    let highlightColor = document.getElementById('highlight-color');
    highlightColor.value = User.highlightColor;
    let backgroundColor = document.getElementById('background-color');
    backgroundColor.value = User.backgroundColor;
    let piecesAColor = document.getElementById('pieces-a-color');
    piecesAColor.value = User.piecesAColor;
    let piecesBColor = document.getElementById('pieces-b-color');
    piecesBColor.value = User.piecesBColor;
};

window.onload = () => {
    // Get the user's profile
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const user_id = urlParams.get('user_id');
    if (user_id == "me") {
        User = getUser();
    } else {
        // const url = `http://localhost:3000/profile/${user_id}` //Not real endpoint
        // fetch(url)
        //     .then(response => response.json())
        //     .then(data => {
        //         User = data;
        //     })
        //     .catch((error) => {
        //         console.error('Error:', error);
        //         alert('An error occurred. Please try again later.');
        //     });
    }

    if (User.victories > 0) {
        // Initialize the interactable JavaScript bits
        let pieces = document.getElementsByClassName('piece');
        let itter_count = 0;
        for (let piece of pieces) {
            piece.addEventListener('click', handleClickPiece);
            if (itter_count < 12) {
                piece.id = `${itter_count + 1}-A`;
            } else {
                piece.id = `${itter_count - 11}-B`;
            }
            itter_count++;
        }

        let customizationStation = document.getElementById('customization-station');
        customizationStation.classList.remove('hidden');
        let nonVictorMessage = document.getElementById('non-victor-message');
        nonVictorMessage.classList.add('hidden');

        // If the player can, but has not yet, customized their pieces
        // Highlight the edit button to signify that there's new stuff in the edit menu
        if (
            User.victories == 1 &&
            User.piecesAColor == "#000000" &&
            User.piecesBColor == "#ffffff" &&
            User.backgroundColor == "#adadad"
        ) {
            const editButton = document.getElementById('edit-button');
            editButton.style.backgroundColor = User.highlightColor;
            // Add animation that makes the background color fade in and out
            editButton.style.animation = 'pulse 3s infinite';
        }
    }

    // const user = getCookie('user');
    const user = User;
    if (user) {
        renderProfile(user);
    } else {
        window.location.href = '/index.html';
    }
}