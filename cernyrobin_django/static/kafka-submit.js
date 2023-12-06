async function fetchData(id) {
    try {
        const response = await fetch(getLocation("/kafka/job?id=", "api") + id);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data); // Process and use your data here

        if (data.percent_completed == 0 || data.percent_completed == 100) {
            document.getElementById('loadingContainer').style.display = 'flex';
            loadingBar.style.display = 'none';
        } else {
            document.getElementById('loadingContainer').style.display = 'none';
            loadingBar.style.display = 'block';
            //updateLoadingBar(data.percent_completed)
            updateLoadingBarAndTime(data.total_chunks, data.chunks_completed)
        }



        // {"video_url": "https://www.youtube.com/watch?v=-WJnehvTnK4", "percent_completed": 14, "chunks_completed": 4, "total_chunks": 29, "finished": false}

        if (data.finished == true) {
            return true
        }
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}

function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}


document.addEventListener('DOMContentLoaded', function () {
    var submitButton = document.getElementById('submit-button');
    var loadingContainer = document.getElementById('loadingContainer');
    var loadingBar = document.getElementById('loadingBar');

    loadingBar.style.display = 'none';




    submitButton.addEventListener('click', function () {
        // loadingContainer.style.visibility = 'visible';
        // document.getElementById('loadContainer').style.visibility = 'visible';
        submitButton.style.visibility = 'hidden';
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

        if (idValid(video_url)) {
            document.getElementById('loadingContainer').style.display = 'flex';
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
        }).then(function (response) {
            console.log(response);
            if (response.headers.get('Content-Type').includes('application/json')) {
                return response.json();
            } else {
                return response.json();
            }
        }).then(function (jsonData) {
            if (jsonData.code == 200) {
                let id = jsonData.message;

                async function continuousFetch(id) {
                    while (true) {
                        let status = await fetchData(id);

                        if (status == true) {
                            // Redirect to view page
                            var view = '/kafka/view?id=' + id;

                            window.location.href = view;

                            break
                        }

                        await sleep(10000); // Sleep for 1000 milliseconds
                    }
                }

                continuousFetch(id)
            } else if (jsonData.code == 201) {
                let id = jsonData.message;

                window.location.href = '/kafka/view?id=' + id;
            } else {
                document.getElementById('submit-response').style.visibility = 'visible';
                document.getElementById('submit-response').textContent = jsonData.message;

                submitButton.style.visibility = 'visible';
                document.getElementById('loadingContainer').style.display = 'none';
                document.getElementById('loadingBar').style.display = 'none';
            }
        });

        // .then(jsonData => jsonData.data).then(function(jsonData) {
        //     if (jsonData && jsonData.answers != undefined) {
        //         var id = jsonData.video_url.split('v=')[1];
        //         var view = '/kafka/view?id=' + id;

        //         document.getElementById('loadingContainer').style.display = 'none';

        //         window.location.href = view
        //     }
        // });
    });

    function getCookie(name) {
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
    }
})
function updateLoadingBar(percent) {
    console.log("defined")
    if (percent > 100 || percent < 0) {
        console.warn("Incorrect percentage value")
    }
    else {
        loadingBar.style.width = percent + '%';
    }

}





function updateLoadingBarAndTime(totalC, doneC) {
    let percent
    if (totalC > 0) {
        percent = doneC / totalC * 100
    }
    else {
        console.log("bullshit passed in")
        percent = -1
    }
    console.log("defined")
    if (percent > 100 || percent < 0) {
        console.warn("Incorrect percentage value")
    }
    else {
        loadingBar.style.width = percent + '%';
    }

}
// {"video_url": "https://www.youtube.com/watch?v=-WJnehvTnK4", "percent_completed": 14, "chunks_completed": 4, "total_chunks": 29, "finished": false}

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