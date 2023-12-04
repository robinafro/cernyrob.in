document.addEventListener('DOMContentLoaded', function() {
    var submitButton = document.getElementById('submit-button');
    var loadingContainer = document.getElementById('loadingContainer');

    submitButton.addEventListener('click', function() {
        // loadingContainer.style.visibility = 'visible';
        // document.getElementById('loadContainer').style.visibility = 'visible';
        submitButton.style.display = 'none';
        document.getElementById('submit-response').style.visibility = 'hidden';

        var video_url = document.getElementById('submit-video-url').value;
        




        //Id validation code
        function idValid(videoUrl) {
            if (!videoUrl) {
                return false;
            }
        



            const standardFormatIndex = videoUrl.indexOf("watch?v=");
            const shortFormatIndex = videoUrl.indexOf("youtu.be/");
        
            if (standardFormatIndex !== -1) {
                const videoId = videoUrl.split("watch?v=")[1].split('&')[0];
                // Check if the videoId is not just an empty string
                return videoId.trim() !== '';
            } else if (shortFormatIndex !== -1) {
                const videoId = videoUrl.split("youtu.be/")[1].split(/[?#]/)[0];
                // Check if the videoId is not just an empty string
                return videoId.trim() !== '';
            }
        
            return false;
        }

        if(idValid(video_url))
        {
            console.log("gg")
            document.getElementById('loadingContainer').style.display = 'flex';
        }
        else{
            console.log("cap")
        }





        var url = '/kafka/submit/';
        
        var headers = new Headers({
            "X-CSRFToken": getCookie("csrftoken"),
        });

        var formData = new FormData();
        formData.append('video_url', video_url);

        fetch(url, {
            method: 'POST',
            body: formData,
            headers: headers
        }).then(function(response) {
            if (response.headers.get('Content-Type').includes('application/json')) {
                return response.json();
            } else {
                response.text().then(function(text) {
                    console.log(text);
                    // document.getElementById('loadContainer').style.visibility = 'hidden';
                    // loadingContainer.style.visibility = 'hidden';
                    //shit
                    document.getElementById('submit-button').style.display = 'block';
                    document.getElementById('submit-response').textContent = text;
                    document.getElementById('submit-response').style.visibility = 'visible';
                });

                return null;
            }
        }).then(jsonData => jsonData.data).then(function(jsonData) {
            if (jsonData && jsonData.answers != undefined) {
                var id = jsonData.video_url.split('v=')[1];
                var view = '/kafka/view?id=' + id;

                window.location.href = view
            }
        });
    });
 
    function getCookie(name) {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
    }
})