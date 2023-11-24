var last_data = null;

function getCSRFToken() {
    const cookieValue = document.cookie
        .split('; ')
        .find((row) => row.startsWith('csrftoken='))
        .split('=')[1];
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    fetch('/get_user_data/?scope=robin_clicker')
        .then(response => response.json())
        .then(data => {
            data = data["data"]
            
            const button = document.getElementById('clicker-button');
            const clickCountElement = document.getElementById('click-count');
            const entireClickText = document.getElementById('total-clicks');

            let counter = parseInt(data["clicks"]);

            button.ondragstart = () => {
                return false;
            };

            button.addEventListener('click', function () {
                if (last_data != null) {
                    if (last_data["clicks"] > counter) {
                        counter = last_data["clicks"];
                    }
                }

                counter++;

                clickCountElement.textContent = counter;

                entireClickText.classList.remove('red');

                setTimeout(() => {
                    entireClickText.classList.add('red');
                }, 1);

                fetch('/clicker/add_click', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken(),
                    },
                })
                .then(response => response.json())
                .then(data => {
                    last_data = data.player_data;

                    if (data.status == "rate_limited") {
                        counter = parseInt(data.player_data["clicks"]);
                        clickCountElement.textContent = counter;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });;

            });

            clickCountElement.textContent = counter
        })
        .catch(error => console.error('Error:', error));
});
