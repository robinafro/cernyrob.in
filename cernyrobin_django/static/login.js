document.addEventListener("DOMContentLoaded", function () {
    var redirect = document.getElementById('login-destination').innerHTML;
    
    if (document.getElementById('auth-text') != null) {
        window.location.replace(redirect)
    }

    var loginButton = document.getElementById('login-button');
    var loginWarning = document.getElementById('login-warning');
    var username = document.getElementById('login-username');
    var password = document.getElementById('login-password');

    loginButton.addEventListener('click', function () {
        if (username.checkValidity() && password.checkValidity() && username.value.length >= 3 && password.value.length >= 3 && username.value.length <= 20 && password.value.length <= 20) {
            // Make a URL-encoded string for passing POST data:
            var dataString = "username=" + encodeURIComponent(username.value) + "&password=" + encodeURIComponent(password.value) + "&redirect=" + encodeURIComponent(redirect); // Not used anymore

            const formData = new FormData();
            formData.append("username", username.value);
            formData.append("password", password.value);

            fetch("login/submit/", {
                method: 'POST',
                body: formData,
                credentials: "include",
            }).then(function (response) {
                // response.text() returns a new promise that resolves with the full response text
                // when it loads. We further process this text in the .then callback.
                response.text().then(function (text) {
                    if (text === "OK") {
                        window.location.replace(redirect)
                    } else {
                        document.getElementById("login-password").value = "";
                        loginWarning.innerHTML = text;
                    }
                });
            });
        } else {
            loginWarning.innerHTML = "kamo tohle fakt nejde sorry";
        };
    });

    username.addEventListener('input', function () {
        if (username.value == "") {
            loginWarning.innerHTML = "aspoň tam něco napiš"
        } else if (!username.checkValidity()) {
            loginWarning.innerHTML = "kamo nepiš tam sračky";
            console.log(loginWarning.value)
        } else if (username.value.length > 20) {
            loginWarning.innerHTML = "to už je moc dlouhý";
        } else if (username.value.length < 3) {
            loginWarning.innerHTML = "tiny ass username";
        }
        else {
            loginWarning.innerHTML = "";
        }
    });

    password.addEventListener('input', function () {
        if (password.value == "") {
            loginWarning.innerHTML = "aspoň tam něco napiš"
        } else if (!password.checkValidity()) {
            loginWarning.innerHTML = "kamo nepiš tam mezery";
            console.log(loginWarning.value)
        } else if (password.value.length > 20) {
            loginWarning.innerHTML = "to už je moc dlouhý";
        } else if (password.value.length < 3) {
            loginWarning.innerHTML = "tiny ass password";
        }
        else {
            loginWarning.innerHTML = "";
        }
    })

    loginWarning.innerHTML = "";
})