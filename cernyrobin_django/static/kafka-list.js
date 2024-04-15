var ads = [
    { image: "kytara.png", link: "https://www.youtube.com/watch?v=I0XACay6e3w" },
    { image: "kytara2.png", link: "https://www.youtube.com/watch?v=QjAn2aMh3ug" },
    { image: "kytara3.png", link: "https://www.youtube.com/watch?v=-YI6MRuBDrg" },
    { image: "kytara4.png", link: "https://www.youtube.com/watch?v=qgbPi627zMU" },
    { image: "robot.png", link: "https://www.youtube.com/watch?v=dQw4w9WgXcQ" },
    { image: "robot2.png", link: "https://www.youtube.com/watch?v=QjAn2aMh3ug" },
    { image: "clicker_ad.jpg", link: "https://autokafka.cz/clicker" },
    { image: "slovak.png", link: "https://slovakje.best/minesweeper" },
    { image: "slovak2.png", link: "https://slovakje.best/clicker" },
];

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
    let ad = ads[Math.floor(Math.random() * ads.length)]
    console.log(ad);
    var template = document.getElementById(templateId);
    var container = template.parentNode;

    var cloned = template.cloneNode(true);
    
    let img = cloned.getElementsByClassName("rekl-image")[0];

    cloned.id = "";
    cloned.style.display = "block";
    img.src = "/static/assets/kafka/" + ad.image;

    container.appendChild(cloned);

    cloned.addEventListener("click", function() {
        window.location.href = ad.link;
    })
}

function loadAds() {
    var contentHeight = document.getElementById("content").clientHeight;
    var ad = document.getElementsByClassName("side-rekl")[0];
    var adContainer = document.getElementById("ad-container");
    var adHeight = adContainer.clientWidth / (1/2) + convertRemToPixels(4);
    var amountOfAds = Math.floor(contentHeight / adHeight);

    console.log(contentHeight);
    console.log(adHeight);
    console.log(amountOfAds);

    for (var i = 0; i < amountOfAds; i++) {
        cloneAd("rekl-left");
        cloneAd("rekl-right");
    }
}

document.addEventListener("DOMContentLoaded", function() {
    loadAds();
})
