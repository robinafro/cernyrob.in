var DESCRIPTION_MAX_LENGTH = 270;

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
        clonedImage.src = image;
    }

    container.appendChild(clonedElement);
}

document.addEventListener("DOMContentLoaded", function() {
    fetch("http://api.localhost:8000/kafka/list")
        .then(data => {
            if (data.status == 200) {
                return data.json();
            } else {
                throw new Error("Something went wrong");
            }
        })
        .then(data => {
            var list = data["list"];

            for (var key in list) {
                var element = list[key];
                var videoInfo = element["video_info"];
                
                var shortedDescription = videoInfo.description.substring(0, DESCRIPTION_MAX_LENGTH) + (videoInfo.description.length > DESCRIPTION_MAX_LENGTH ? "..." : "");

                cloneElement(videoInfo.id, videoInfo.title, shortedDescription, videoInfo.thumbnail_url);
            }
        })
})
