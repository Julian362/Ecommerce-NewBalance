function ratingEstrella(num, option, reference,documento){
    for (let i = 1; i <= num; i++) {
        document.getElementById("estrella"+i).innerHTML="★";
    }
    document.getElementById("gestionarComentario").action="/comentario/gestionar/"+option.toLowerCase()+"/"+reference+"-"+num+"-"+documento;
    for (let i = num+1; i <= 5; i++) {
        document.getElementById("estrella"+i).innerHTML="☆";
    }
}

