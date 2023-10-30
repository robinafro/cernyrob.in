document.addEventListener('DOMContentLoaded', function () {
    var playerData = null
        
    fetch('/get_player_data')
    .then(response => response.json())
    .then(data => {
        playerData = data.player_data;
        console.log(playerData);
    })
    .catch(error => console.error('Error:', error));

    const button = document.getElementById('clicker-button');
    const clickCountElement = document.getElementById('click-count');
    const entireClickText = document.getElementById('total-clicks');

    let counter = parseInt(playerData["clicks"]);

    button.addEventListener('click', function () {
        counter++;

        clickCountElement.textContent = counter;

        entireClickText.classList.remove('red');

        setTimeout(() => {
            entireClickText.classList.add('red');
        }, 1);

        fetch('/add_click', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ action: 'add_click' }),
        });

    });

    clickCountElement.textContent = counter
});
