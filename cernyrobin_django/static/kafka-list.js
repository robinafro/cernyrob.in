var ads = [
    "kytara.png",
    "kytara2.png",
    "kytara3.png",
    "kytara4.png",
    "robot.png",
    "robot2.png",
    "clicker_ad.jpg",
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
    loadAds();
})
