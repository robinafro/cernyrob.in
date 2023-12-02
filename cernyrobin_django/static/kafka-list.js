var ads = [
    "kytara.png",
    "kytara2.png",
    "kytara3.png",
    "kytara4.png",
    "robot.png",
    "robot2.png",
]

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

function convertRemToPixels(rem) {    
    return rem * parseFloat(getComputedStyle(document.documentElement).fontSize);
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

    container.insertBefore(clonedElement, originalElement);

    clonedElement.addEventListener("click", function() {
        window.location.href = getLocation("/kafka/view?id=" + id);
    })
}

function cloneAd(templateId) {
    var template = document.getElementById(templateId);
    var container = template.parentNode;

    var cloned = template.cloneNode(true);

    cloned.id = "";
    cloned.style.display = "block";
    cloned.src = "/static/assets/kafka/" + ads[Math.floor(Math.random() * ads.length)];

    container.appendChild(cloned);
}

function loadAds() {
    var contentHeight = document.getElementById("content").clientHeight;
    var ad = document.getElementsByClassName("side-ad")[0];
    var adContainer = document.getElementById("ad-container");
    var adHeight = adContainer.clientWidth / (1/2) + convertRemToPixels(4);
    var amountOfAds = Math.floor(contentHeight / adHeight);

    console.log(contentHeight);
    console.log(adHeight);
    console.log(amountOfAds);

    for (var i = 0; i < amountOfAds; i++) {
        cloneAd("ad-left");
        cloneAd("ad-right");
    }
}

document.addEventListener("DOMContentLoaded", function() {
    var addVideoButton = document.getElementById("kafka-list-add-video-button");

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

            loadAds();
        })

    addVideoButton.addEventListener("click", function() {
        window.location.href = getLocation("/kafka/submit");
    })
})
