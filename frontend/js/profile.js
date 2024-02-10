const handleClickPiece = (event) => {
    // Get the piece that was clicked
    // Open up a menu allowing the user to edit the piece's text
    // (and possibly view per-piece stats)
    // ONLY AVAILABLE TO VICTORS
    console.log(event.target);
};

const handleLogoutClicked = () => {
    document.cookie = null;
    window.location.href = 'login.html'
}

const handleEditClicked = () => {
    alert('Edit clicked');
    // Show Hidden Edit Fields
    // Hide the Shown non-edit fields
};

const handleSaveClicked = () => {
};

const handleCancelClicked = () => {
};

const handleDeleteClicked = () => {
};

window.onload = () => {
    // Get the user's profile
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
}