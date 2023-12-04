function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}


function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

document.addEventListener('DOMContentLoaded', function() {

    if(getCookie("hideDisclaimer") === "true"){
        document.getElementById('disclaimer-footer').style.visibility = 'hidden';
        console.log("hidden auto")
    }

    document.getElementById('disclaimer-button').addEventListener('click', function() {

        document.getElementById('disclaimer-footer').style.visibility = 'hidden';
        setCookie("hideDisclaimer", "true", 3); 
        console.log("hidden man")

})})



