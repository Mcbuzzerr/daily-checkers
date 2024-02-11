const handleLoginClicked = () => {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const data = { email: email, password };
    const url = "http://localhost:3000/login" //Not real endpoint
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                setCookie('user', JSON.stringify(data.user), 22);
                window.location.href = '/profile.html';
            } else {
                alert('Invalid username or password');
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again later.')
        });
}