document.addEventListener("DOMContentLoaded", function () {
    var loginButton = document.getElementById('login-button');
    var loginWarning = document.getElementById('login-warning');
    var username = document.getElementById('login-username');
    var password = document.getElementById('login-password');

    loginButton.addEventListener('click', function () {
        if (username.checkValidity() && password.checkValidity() && username.value.length >= 3 && password.value.length >= 3 && username.value.length <= 20 && password.value.length <= 20) {
            const formData = new FormData();
            formData.append("username", username.value);
            formData.append("password", password.value);

            var headers = new Headers({
                "X-CSRFToken": getCookie("csrftoken"),
            });

            fetch("/login/submit/", {
                method: 'POST',
                body: formData,
                credentials: "include",
                headers: headers,
            }).then(function (response) {
                // response.text() returns a new promise that resolves with the full response text
                // when it loads. We further process this text in the .then callback.
                response.text().then(function (text) {
                    if (text === "200 OK") {
                        ////
                    } else {
                        document.getElementById("login-password").value = "";
                        loginWarning.innerHTML = text;
                    }
                });
            });
        } else {
            loginWarning.innerHTML = "kamo tohle fakt nejde sorry";
        };

        function getCookie(name) {
            var value = "; " + document.cookie;
            var parts = value.split("; " + name + "=");
            if (parts.length == 2) return parts.pop().split(";").shift();
        }
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