console.log("loaded")
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

