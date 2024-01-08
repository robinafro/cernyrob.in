document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        document.getElementById("info").style.display = "block";
        console.log("displaying popup");
    }, 5000);
});

function closePopup() {
    document.getElementById("info").style.display = "none";
}
