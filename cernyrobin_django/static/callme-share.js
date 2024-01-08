document.addEventListener('DOMContentLoaded', function() {
    var shareLink = document.getElementById('share-link');
    var linkDisplay = document.getElementById('link-display');

    var linkText = shareLink.textContent;
    if (linkText.startsWith('https://')) {
        linkText = linkText.substring(8);
    } else if (linkText.startsWith('http://')) {
        linkText = linkText.substring(7);
    }
    
    linkDisplay.textContent = linkText;
});