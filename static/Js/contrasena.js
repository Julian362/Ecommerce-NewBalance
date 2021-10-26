function mostrarContrasena() {
    var con = document.getElementById("contrasena");
    if (con.type === "password") {
        con.type = "text";
    } else {
        con.type = "password";
    }
    var conc = document.getElementById("confirmarContrasena");
    if (conc.type === "password") {
        conc.type = "text";
    } else {
        conc.type = "password";
    }
    var conc = document.getElementById("contrasenaNueva");
    if (conc.type === "password") {
        conc.type = "text";
    } else {
        conc.type = "password";
    }
}