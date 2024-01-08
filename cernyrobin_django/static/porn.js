document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        document.getElementById("info").style.display = "flex";
        console.log("displaying popup");
    }, 500);


    var div = document.getElementById('info');
var isLarge = false; // State tracking variable

function toggleSize() {
  // Change the size of the div based on its current state
  div.style.width = isLarge ? '30%' : '35%';
/*   div.style.height = isLarge ? '200px' : '300px'; */

  isLarge = !isLarge; // Toggle state
}

//setInterval(toggleSize, 100); // Adjust the size every 1 second

setInterval(toggleSize, 1000);

});

function closePopup() {
    document.getElementById("info").style.display = "none";
}
