//   function changeOpenStatus() {
//     var articles = document.getElementsByClassName("answer-text");
//     for (var i = 0; i < articles.length; i++) {
//       var article = articles[i];
//       if (article.style.maxHeight) {
//         article.style.maxHeight = null;
// /*         article.style.margin = "0px 0px -5.5px 0px" */
//       } else {
//         article.style.maxHeight = article.scrollHeight + "px";
// /*         article.style.margin = "3px 3px 3px 3px" */
//       }
//     }
//   }




// function changeOpenStatus() {
//     let answerTextElement = this.parentElement.parentElement.querySelector('.answer-text');
//     console.log(answerTextElement);
//     if (article.style.maxHeight) {
//      article.style.maxHeight = null;

//             } else {
//               article.style.maxHeight = article.scrollHeight + "px";


//             }
//           }

  function changeOpenStatusBulk(open) {
    var articles = document.getElementsByClassName("answer-text");
    var button = document.getElementById("bulk-collapse-menu");
    for (var i = 0; i < articles.length; i++) {
      var article = articles[i];
      if (!open) {
        article.style.maxHeight = null;
        button.innerHTML = "⮟"; //⮟⮝
/*         article.style.margin = "0px 0px -5.5px 0px" */
      } else {
        article.style.maxHeight = article.scrollHeight + "px";
        button.innerHTML = "⮝"; //⮟

/*         article.style.margin = "3px 3px 3px 3px" */
      }
    }
  }



  document.addEventListener("DOMContentLoaded", function () {
    changeOpenStatusBulk(true)

  });



  function copyText() {
    
    // For example, copying some text to the clipboard

    // Show the popup
    var popup = document.getElementById("copyPopup");
    popup.classList.add("show");

    // Hide the popup after 2 seconds
    setTimeout(function(){ popup.classList.remove("show"); }, 2000);
}





// Assume the URL is something like "http://www.example.com/?id=123&category=books"

// Get the query string from the current URL
const queryString = window.location.search;

// Use URLSearchParams to work with the query string
const urlParams = new URLSearchParams(queryString);

// Get the value of the 'id' parameter
const id = urlParams.get('id');

console.log(id);


document.addEventListener("DOMContentLoaded", function () {
  // Your code here
});
