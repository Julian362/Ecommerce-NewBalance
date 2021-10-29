function validar_formulario() {

    var nombre = document.getElementById("nombre");
    var apellido = document.getElementById("apellido");
    var email = document.getElementById("email");
    var nickname = document.getElementById("nickname")
    var documento = document.getElementById("documento")
    var telefono = document.getElementById("telefono")
    var contrasena_original = document.getElementById("contraseña_original");
    var errores = document.getElementById("errores");
    var hayerrores = false

    errores.innerHTML = "";
    if (nombre.value.length == 8 || nombre.value.length < 8) {
        // alert('El nombre debe tener mas de 8 caracteres');
        errores.innerHTML += 'El nombre debe tener mas de 8 caracteres. <br/>';
        nombre.className = "errores";
        // return false;
        hayerrores = true;
    }

    if (apellido.value.length == 8 || apellido.value.length < 8) {
        // alert('El apellido debe tener mas de 8 caracteres');
        errores.innerHTML += 'El apellido debe tener mas de 8 caracteres. <br/>';
        apellido.className = "errores";
        // return false;
        hayerrores = true;
    }

    var formato_email = /^[-\w.%+]{1,64}@(?:[A-Z0-9-]{1,63}\.){1,125}[A-Z]{2,63}$/i;
    if (!email.value.match(formato_email)) {
        // alert('Debe especificar un correo valido');
        errores.innerHTML += 'El email debe tener mas de 8 caracteres. <br/>';
        email.className = "errores";
        // return false;
        hayerrores = true;
    }

    if (contrasena.value.length == 8 || contrasena.value.length < 8) {
        // alert('La contraseña debe tener mas de 8 caracteres');
        errores.innerHTML += 'La contraseña debe tener mas de 8 caracteres <br/>';
        contrasena.className = "errores";
        // return false;
        hayerrores = true;
    }

    return !hayerrores;




}