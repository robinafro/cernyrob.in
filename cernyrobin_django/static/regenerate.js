document.addEventListener('DOMContentLoaded', function () {
    let regenerateButton = document.getElementById('regen-button');

    regenerateButton.addEventListener('click', function () {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const id = urlParams.get('id');
        const video_url = "youtube.com/watch?v=" + id

        var headers = new Headers({
            "X-CSRFToken": getCookie("csrftoken"),
        });

        var formData = new FormData();
        formData.append('video_url', video_url);

        fetch('/kafka/regenerate/', {
            method: 'POST',
            body: formData,
            headers: headers
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
            });
    })
})

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}