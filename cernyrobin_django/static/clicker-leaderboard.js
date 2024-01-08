function cloneLeaderboardElement(name, clicks) {
    var leaderboardContainer = document.getElementById("clicker-leaderboard");
    var originalLeaderboardElement = document.querySelector(".leaderboard-element");

    // Clone the original element
    var clonedElement = originalLeaderboardElement.cloneNode(true);

    clonedElement.style.display = "flex";

    var clonedKey = clonedElement.querySelector(".leaderboard-key");
    var clonedValue = clonedElement.querySelector(".leaderboard-value");

    // Update the texts as needed
    clonedKey.textContent = name;
    clonedValue.textContent = clicks;

    leaderboardContainer.appendChild(clonedElement);
}

document.addEventListener('DOMContentLoaded', function () {
    fetch('/get_user_data/?scope=robin_clicker')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            
            var localUsername = data["username"];
            var clickerData = data["data"];

            fetch('/get_all_data/?scope=robin_clicker')
                .then(response => response.json())
                .then(data => {
                    // Convert the object to an array of objects
                    var dataArray = Object.entries(data).map(([key, value]) => ({
                        user: key,
                        ...value
                    }));

                    console.log("All data:");
                    console.log(dataArray);

                    // Sort the array in descending order based on the "clicks" property
                    var sortedData = dataArray.sort((a, b) => b.data.clicks - a.data.clicks);

                    console.log("Sorted data:");
                    console.log(sortedData);

                    var localPlayerIsInTop10 = false;

                    // Process the sorted array
                    for (var i = 0; i < sortedData.length; i++) {
                        var playerData = sortedData[i];

                        if (playerData.username == localUsername) {
                            localPlayerIsInTop10 = true;
                        }
                        
                        cloneLeaderboardElement((i + 1) + ". " + playerData.username, playerData.data.clicks);
                    }

                    if (!localPlayerIsInTop10) {
                        cloneLeaderboardElement((sortedData.length + 1) + ". " + localUsername, clickerData.clicks);
                    }
                });
        })
});