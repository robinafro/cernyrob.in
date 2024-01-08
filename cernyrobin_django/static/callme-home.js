document.addEventListener('DOMContentLoaded', function () {
    fetch('/get_data', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            var callmeData = data.callme_data;

            var addNumber = document.getElementById('add-number');
            var shareNumber = document.getElementById('share-number');
            var deleteNumber = document.getElementById('delete-number');
            var addNumberText = document.getElementById('add-number-text');
            var addNumberLink = document.getElementById('add-number-link');

            if (callmeData["phone_number"] == null) {
                addNumberText.textContent = "Add number";

                addNumberLink.setAttribute("href", "/create");

                deleteNumber.style.display = "none";
            } else {
                addNumberText.textContent = "Edit info";

                addNumberLink.setAttribute("href", "/edit");
            }
        })
        .catch(error => console.error('Error:', error));
});