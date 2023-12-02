function getLocation(path, subdomain) {
    var currentHostname = window.location.hostname;
    var currentPort = window.location.port;
    var currentScheme = window.location.protocol;

    if (subdomain == null) {
        return currentScheme + "//" + currentHostname + ":" + currentPort + path;
    } else {
        return currentScheme + "//" + subdomain + "." + currentHostname + ":" + currentPort + path;
    }
}

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

    clonedElement.addEventListener("click", function() {
        window.location.href = getLocation("/kafka/view?id=" + id);
    })
}

document.addEventListener("DOMContentLoaded", function() {
    console.log(getLocation("/kafka/list", "api"))
    fetch(getLocation("/kafka/list", "api"))
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

                cloneElement(key.split("v=")[1], videoInfo.title, videoInfo.description, videoInfo.thumbnail_url);
            }
        })
})
