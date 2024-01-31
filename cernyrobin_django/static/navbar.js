function changeOpenStatusSide() {
    var articles = document.getElementById("sidebar-dropdown-container");
    for (var i = 0; i < articles.length; i++) {
      var article = articles[i];
      if (article.style.maxHeight) {
        article.style.maxHeight = null;
        console.log("hidden")
/*         article.style.margin = "0px 0px -5.5px 0px" */
      } else {
        article.style.maxHeight = article.scrollHeight + "px";
/*         article.style.margin = "3px 3px 3px 3px" */
console.log("showed")
      }
    }
  }


  document.addEventListener("DOMContentLoaded", function () {
    changeOpenStatusSide()
  });



  
document.getElementById('hamburger-menu').addEventListener('click', function() {
    console.log(document.getElementById('sidebar').style.width)
    if (document.getElementById('sidebar').style.width == "0px" || document.getElementById('sidebar').style.width == ""){
        document.getElementById('sidebar').style.width = '250px';
        // document.getElementById('main-content').style.marginLeft= '0';
        // this.style.display = 'none';
        // document.getElementById('hamburger-menu').style.display = 'block';
    }
    else{
        document.getElementById('sidebar').style.width = '0';
    }
    });





