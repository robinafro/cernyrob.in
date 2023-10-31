document.addEventListener("DOMContentLoaded", function () {
    var loginButton = document.getElementById('login-button');
    var redirect = "clicker"

    loginButton.addEventListener('click', function () {
        console.log("Clicked");
        var username = document.getElementById('login-username').value;
        var password = document.getElementById('login-password').value;

        // Make a URL-encoded string for passing POST data:
        var dataString = "username=" + encodeURIComponent(username) + "&password=" + encodeURIComponent(password) + "&redirect=" + encodeURIComponent(redirect);

        fetch("/auth", {
            method: 'POST',
            body: dataString,
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        }).then(function (response) {
            // response.text() returns a new promise that resolves with the full response text
            // when it loads. We further process this text in the .then callback.
            response.text().then(function (text) {
                if (text === "OK") {
                    console.log("Successful login");
                } else {
                    document.getElementById("login-password").placeholder = text;
                }
            });
        });
    });
})