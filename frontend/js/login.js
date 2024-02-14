const handleLoginClicked = () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const data = { email: email, password };
    const url = "http://localhost:3000/login" //Not real endpoint
    let user = null;
    // fetch(url, {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify(data),
    // })
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data.success) {
    //             user = data.user;
    //             window.location.href = '/profile.html?user=me';
    //         } else {
    //             alert('Invalid username or password');
    //         }
    //     }).catch(error => {
    //         console.error('Error:', error);
    //         alert('An error occurred. Please try again later.')
    //     });

    user = {
        "id": "213123-123123-123123-123213", //Friend Code
        "name": "Player A",
        "email": "playerA@email.com",
        "password": "shhhhhhhhhhhhh",
        "victories": 1,
        "pieces": [
            {
                "id": "1-A", // {PieceNumber}-{TeamLetter} A = Black, B = White
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "2-A",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "3-A",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "4-A",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "5-A",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "6-A",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "7-A",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "8-A",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "9-A",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "10-A",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "11-A",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "12-A",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "1-B",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "2-B",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "3-B",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "4-B",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "5-B",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "6-B",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "7-B",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "8-B",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "9-B",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "10-B",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "11-B",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            },
            {
                "id": "12-B",
                "displayText": "text",
                "lifetimeKills": 0,
                "lifetimeDeaths": 0,
                "lifetimePromotions": 0
            }
        ],
        "piecesAColor": "#000000",
        "piecesBColor": "#ffffff",
        "highlightColor": "#ffe600",
        "backgroundColor": "#adadad"
    };

    setUser(user);
    window.location.href = '/profile.html?user=me';
}