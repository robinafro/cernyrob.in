let counter = 0;

document.addEventListener('DOMContentLoaded', function () {
    const button = document.getElementById('clicker-button');
    const counterDisplay = document.getElementById('total-clicks');

    button.addEventListener('click', function () {
        counter++;

        counterDisplay.textContent = "Your clicks: " + counter;

        counterDisplay.classList.remove('red');

        setTimeout(() => {
            counterDisplay.classList.add('red');
        }, 1);
    });
});