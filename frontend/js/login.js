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
        "name": "Player Template",
        "email": "playerA@email.com",
        "password": "shhhhhhhhhhhhh",
        "victories": 1,
        "pieces": {
            "1-A": { // {PieceNumber}-{TeamLetter} A = Black, B = Whit: {

                "displayText": "",
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
    };

    setUser(user);
    window.location.href = '/frontend/profile.html';
}