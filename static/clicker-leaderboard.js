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
    fetch('/get_player_data')
        .then(response => response.json())
        .then(data => {
            var player_data = data.player_data;
            var userData = player_data["user_data"];
            var clickerData = player_data["robin_clicker"];

            fetch('/get_all_clicker_data/10')
                .then(response => response.json())
                .then(data => {
                    var allData = data.all_clicker_data;

                    // Convert the object to an array of objects
                    var dataArray = Object.entries(allData).map(([key, value]) => ({
                        id: key,
                        ...value
                    }));

                    console.log("All data:");
                    console.log(dataArray);

                    // Sort the array in descending order based on the "clicks" property
                    var sortedData = dataArray.sort((a, b) => b.clicks - a.clicks);

                    console.log("Sorted data:");
                    console.log(sortedData);

                    var localPlayerIsInTop10 = false;

                    // Process the sorted array
                    for (var i = 0; i < sortedData.length; i++) {
                        var playerData = sortedData[i];

                        if (playerData.name == userData.username) {
                            localPlayerIsInTop10 = true;
                        }

                        // Assuming cloneLeaderboardElement takes two arguments: name and clicks
                        cloneLeaderboardElement((i + 1) + ". " + playerData.name, playerData.clicks);
                    }

                    if (!localPlayerIsInTop10) {
                        cloneLeaderboardElement((sortedData.length + 1) + ". " + userData.username, clickerData.clicks);
                    }
                });
        })
});