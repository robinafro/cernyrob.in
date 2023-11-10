document.addEventListener('DOMContentLoaded', function () {
    var name = document.getElementById('nickname');
    var phoneNumber = document.getElementById('phone_number');
    var submit = document.getElementById('submit');
    var title = document.getElementById('callme-create-title');


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
        }
    });

    submit.addEventListener('click', function () {
        var data = {
            name: name.value,
            phoneNumber: phoneNumber.value.replace(" ", "")
        }; // Todo fix replace(" ", ""), proper validation of both fields

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
});