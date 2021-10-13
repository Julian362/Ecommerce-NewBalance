function abrir1(){
    document.getElementById("tab1").style.display="block";
    document.getElementById("tab2").style.display="none";
    document.getElementById("pri").style.background="#cccccc";
    document.getElementById("pri").style.color="red";
    document.getElementById("sda").style.background="none";
    document.getElementById("sda").style.color="#242942";
}


function abrir2(){
    document.getElementById("tab2").style.display="block";
    document.getElementById("tab1").style.display="none";
    document.getElementById("pri").style.background="none";
    document.getElementById("pri").style.color="#242942";
    document.getElementById("sda").style.background="#cccccc";
    document.getElementById("sda").style.color="red";
}

