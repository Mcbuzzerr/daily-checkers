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
};

const renderProfile = (user) => {
    let nameElement = document.getElementById('playerName');
    nameElement.innerText = user.name;
    let friendCodeElement = document.getElementById('friendCode');
    friendCodeElement.innerText = user.id;
    let playerWinsElement = document.getElementById('player-victories');
    playerWinsElement.innerText = user.victories;


    let playerPieces = user.pieces;
    let pieces = document.getElementsByClassName('piece');
    let itter_count = 0;
    for (let piece of pieces) {
        piece.innerText = playerPieces[itter_count].displayText;
        itter_count++;
    }

    // Set the colors
    document.documentElement.style.setProperty('--player-a-piece-color-primary', user.piecesAColor);
    document.documentElement.style.setProperty('--player-b-piece-color-primary', user.piecesBColor);
    document.documentElement.style.setProperty('--current-player-outline-color', user.highlightColor);
    document.documentElement.style.setProperty('--current-player-background-color', user.backgroundColor);

    // Set field values
    let playerIdElement = document.getElementById('player-id');
    playerIdElement.innerHTML = user.id;
    let playerNameField = document.getElementById('name-field');
    playerNameField.value = user.name;
    let playerEmailField = document.getElementById('email-field');
    playerEmailField.value = user.email;
    let highlightColor = document.getElementById('highlight-color');
    highlightColor.value = user.highlightColor;
    let backgroundColor = document.getElementById('background-color');
    backgroundColor.value = user.backgroundColor;
    let piecesAColor = document.getElementById('pieces-a-color');
    piecesAColor.value = user.piecesAColor;
    let piecesBColor = document.getElementById('pieces-b-color');
    piecesBColor.value = user.piecesBColor;
};

window.onload = () => {
    // Get the user's profile
    let PlayerA_inDB = {
        "id": "213123-123123-123123-123213", //Friend Code
        "name": "Player A",
        "email": "playerA@email.com",
        "password": "shhhhhhhhhhhhh",
        "victories": 0,
        "pieces": [
            {
                "id": "1-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "2-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "3-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "4-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "5-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "6-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "7-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "8-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "9-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "10-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "11-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "12-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            },
            {
                "id": "1-B", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "2-B", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "3-B", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "4-B", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "5-B", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "6-B", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "7-B", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "8-B", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "9-B", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "10-B", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "11-B", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }, // List of pieces includes black and white
            {
                "id": "12-B", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
            }
        ],
        "piecesAColor": "#000000",
        "piecesBColor": "#ffffff",
        "highlightColor": "#ffe600",
        "backgroundColor": "#adadad",
    }


    if (PlayerA_inDB.victories > 0) {
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
            PlayerA_inDB.victories == 1 &&
            PlayerA_inDB.piecesAColor == "#000000" &&
            PlayerA_inDB.piecesBColor == "#ffffff" &&
            PlayerA_inDB.backgroundColor == "#adadad"
        ) {
            const editButton = document.getElementById('edit-button');
            editButton.style.backgroundColor = PlayerA_inDB.highlightColor;
            // Add animation that makes the background color fade in and out
            editButton.style.animation = 'pulse 3s infinite';
        }
    }

    // const user = getCookie('user');
    const user = PlayerA_inDB;
    if (user) {
        renderProfile(user);
    } else {
        window.location.href = '/index.html';
    }
}