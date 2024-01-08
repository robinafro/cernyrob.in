document.addEventListener('DOMContentLoaded', function () {
    var name = document.getElementById('nickname');
    var phoneNumber = document.getElementById('phone_number');
    var submit = document.getElementById('submit');
    var title = document.getElementById('callme-create-title');
    var err = document.getElementById('callme-create-error');

    fetch('/get_data', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(function (response) {
        return response.json();
    }).then(function (data) {
        var callmeData = data.callme_data;

        if (callmeData["phone_number"] == null) {
            title.textContent = "create";
        } else {
            title.textContent = "edit";
            name.value = callmeData["name"];
            phoneNumber.value = callmeData["phone_number"];
        }
    });

    submit.addEventListener('click', function () {
        fetch('/create/', {
            method: 'POST',
            body: "name=" + encodeURIComponent(name.value) + "&phone_number=" + encodeURIComponent(phoneNumber.value),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
        }).then(function (data) {
            console.log(data)
            if (data.status == 200) {
                window.location.href = "/";
            }
        });
    });

    name.addEventListener('input', function () {
        if (name.value.length == 0) {
            err.textContent = "Name cannot be empty";
        } else if (name.value.length > 20) {
            err.textContent = "Name is too long";
        } else if (!name.checkValidity()) {
            err.textContent = "Name contains invalid characters";
        } else {
            err.textContent = "";
        }
    });

    phoneNumber.addEventListener('input', function () {
        var phonePattern = /^\+?[1-9][0-9]{7,14}$/;
        var noSpaces = phoneNumber.value.replace(/\s/g, "");

        if (phoneNumber.value.length == 0) {
            err.textContent = "Phone number cannot be empty";
        } else if (phoneNumber.value.length > 20) {
            err.textContent = "Phone number is too long";
        } else if (!phonePattern.test(noSpaces)) {
            err.textContent = "Phone number is invalid";
        } else {
            err.textContent = "";
        }
    });
});