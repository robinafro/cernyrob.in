/* 
    openStatus = true
    function changeOpenStatus() {
        var article = document.getElementsByClassName("answer-text")
        if (article.style.maxHeight){
          article.style.maxHeight = null;
        } else {
          article.style.maxHeight = article.scrollHeight + "px";
        } 
      }
    
 */

  console.log("loaded")


  function changeOpenStatus() {
    console.log("ran")
    var articles = document.getElementsByClassName("answer-text");
    for (var i = 0; i < articles.length; i++) {
      var article = articles[i];
      if (article.style.maxHeight) {
        article.style.maxHeight = null;
      } else {
        article.style.maxHeight = article.scrollHeight + "px";
      }
    }
  }


  document.addEventListener("DOMContentLoaded", function () {
    changeOpenStatus()
  });