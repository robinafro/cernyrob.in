function cloneElement(id, name, description, image) {
    var container = document.getElementById("page-container");
    var originalElement = document.getElementById("element-template");

    // Clone the original element
    var clonedElement = originalElement.cloneNode(true);

    clonedElement.id = id
    clonedElement.style.display = "flex";

    var clonedName = clonedElement.querySelector(".kafka-list-element-title");
    var clonedDescription = clonedElement.querySelector(".kafka-list-element-description");
    var clonedImage = clonedElement.querySelector(".kafka-list-element-image");

    // Update the texts as needed
    clonedName.textContent = name;
    clonedDescription.textContent = description;

    if (image != null) {
        clonedImage.textContent = image;
    }

    container.appendChild(clonedElement);
}

document.addEventListener("DOMContentLoaded", function() {
    fetch("http://api.localhost:8000/kafka/list", {
        mode: "no-cors"
    })
        .then(data => {
            console.log(data);
            data = data["list"];
        })
})
