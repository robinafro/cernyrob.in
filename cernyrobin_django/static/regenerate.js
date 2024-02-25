function startLoadingAnimation() {
    console.log('startLoadingAnimation')
    const loadingElement = document.getElementById('loading-text');
    const regenButton = document.getElementById('regen-button');
    regenButton.style.opacity = 0;
    setTimeout(function() {
        // This code will be executed after 2 seconds
        console.log("This is a delayed message.");
        
        regenButton.style.display = 'none';
        loadingElement.style.display = 'block';
        
        let dotCount = 0;
        
        // Clear any existing intervals to prevent multiple instances running
        if (window.loadingInterval) clearInterval(window.loadingInterval);
        
        window.loadingInterval = setInterval(() => {
            dotCount = (dotCount % 4) + 1; // Cycle through 1 to 3
            loadingElement.innerHTML = 'Generují se nové odpovědi' + '.'.repeat(dotCount-1) + "&nbsp;".repeat(4-dotCount);
        }, 500); // Adjust the speed as needed
    }, 2000);
  }


document.addEventListener('DOMContentLoaded', function () {
    let regenerateButton = document.getElementById('regen-button');

    regenerateButton.addEventListener('click', function () {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const id = urlParams.get('id');
        const video_url = "youtube.com/watch?v=" + id

        var headers = new Headers({
            "X-CSRFToken": getCookie("csrftoken"),
        });

        var formData = new FormData();
        formData.append('video_url', video_url);

        startLoadingAnimation();
        fetch('/kafka/regenerate/', {
            method: 'POST',
            body: formData,
            headers: headers
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
            });
    
    setInterval(() => {
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const videoId = urlParams.get('id');
        const providedUsername = document.getElementById('username-provider').innerText

        let endpointPath = `/kafka/job?id=${videoId}${providedUsername}`
        console.log(endpointPath)
        fetch(endpointPath)
            .then(response => response.json())
            .then(data => {
                if (data.finished){

                    window.location.replace(window.location.href.replace('view/', 'view/custom/'))
                                    
                    
                }
            });
    }, 1000); // Adjust the interval as needed
        
        })
    })

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}
