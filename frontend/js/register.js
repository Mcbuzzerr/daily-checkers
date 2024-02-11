const handleRegisterClicked = () => {

    const email = document.getElementById('email').value;
    const name = document.getElementById('name').value;
    const password = document.getElementById('password').value;

    const data = {
        email,
        name,
        password
    };

    //Not real endpoint
    const url = "http://localhost:3000/register"
    //Not real endpoint

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => {
        if (response.status === 200) {
            alert('User registered successfully');
            window.location.href = '/login';
        } else {
            response.json().then(data => {
                alert(data.message);
            });
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again later.')
    });
}