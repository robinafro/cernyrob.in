var last_data = null;

document.addEventListener('DOMContentLoaded', function () {
    fetch('/get_player_data')
        .then(response => response.json())
        .then(data => {
            var playerData = data.player_data;

            const button = document.getElementById('clicker-button');
            const clickCountElement = document.getElementById('click-count');
            const entireClickText = document.getElementById('total-clicks');

            let counter = parseInt(playerData["clicks"]);

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

                fetch('/add_click', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
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
