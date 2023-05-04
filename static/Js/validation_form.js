window.onload = function () {

    var password_original = document.getElementById('contraseña_original');
    var password_repetida = document.getElementById('contraseña_repetida');
    var nombre = document.getElementById('nombre');
    var apellido = document.getElementById('apellido');
    var email=document.getElementById('email');
    var nickname=document.getElementById('nickname');
    var telefono=document.getElementById('telefono');
    var pais=document.getElementById('pais');
    var departamento=document.getElementById('departamento');
    var ciudad=document.getElementById('ciudad');
    var direccion=document.getElementById('direccion');
    

    password_repetida.onmouseout= function (){
        if  (password_repetida.value.length==0){
            password_original.style="color:none; border-color:none" 
            password_repetida.style="color:none; border-color:none"
        }
        else if ((password_original.value != password_repetida.value) || (password_original.value.length<8)){
            password_original.style="color:red; border-color:red"
            password_repetida.blur();
            password_repetida.style="color:red; border-color:red"
            Swal.fire('revise que las contraseñas sean iguales o tenga más de 8 caracteres') 
        }        
        else{
            password_original.style="color:green; border-color:green" 
            password_repetida.blur();
            password_repetida.style="color:green; border-color:green"
        }
    }

    documento.onmouseout = function  (){
        if (documento.value.length == 0){
            documento.style="color:none; border-color:none";        }
        else if (documento.value.length < 6){
            documento.style="color:red; border-color:red";
            Swal.fire('El documento debe ser mayor a 6 caracteres')        }
        else{
            documento.style="color:green; border-color:green";
            documento.blur()
        }
    }
    nombre.onmouseout = function  (){
        if (nombre.value.length == 0){
            nombre.style="color:none; border-color:none";        
        }      
        else{
            nombre.style="color:green; border-color:green";
            nombre.blur()
        }
    }
    apellido.onmouseout = function  (){
        if (apellido.value.length == 0){
            apellido.style="color:none; border-color:none";        
        }      
        else{
            apellido.style="color:green; border-color:green";
            apellido.blur()
        }
    }
    email.onmouseout = function  (){
        if (email.value.length == 0){
            email.style="color:none; border-color:none";        
        }      
        else{
            email.style="color:green; border-color:green";
            email.blur()
        }
    }
    nickname.onmouseout = function  (){
        if (nickname.value.length == 0){
            nickname.style="color:none; border-color:none";        
        }      
        else{
            nickname.style="color:green; border-color:green";
            nickname.blur()
        }
    }
    telefono.onmouseout = function  (){
        if (telefono.value.length == 0){
            telefono.style="color:none; border-color:none";        
        }      
        else if (telefono.value.length < 10){
            telefono.style="color:red; border-color:red";
            telefono.blur()
            Swal.fire('revise que el numero tenga mas de 10 caracteres') 
        }
        else{
            telefono.style="color:green; border-color:green";
            telefono.blur()
        }        
    } 
    pais.onmouseout = function  (){
        if (pais.value.length == 0){
            pais.style="color:none; border-color:none";        
        }      
        else{
            pais.style="color:green; border-color:green";
            pais.blur()
        }
    }
    departamento.onmouseout = function  (){
        if (departamento.value.length == 0){
            departamento.style="color:none; border-color:none";        
        }      
        else{
            departamento.style="color:green; border-color:green";
            departamento.blur()
        }
    }
    ciudad.onmouseout = function  (){
        if (ciudad.value.length == 0){
            ciudad.style="color:none; border-color:none";        
        }      
        else{
            ciudad.style="color:green; border-color:green";
            ciudad.blur()
        }
    }
    direccion.onmouseout = function  (){
        if (direccion.value.length == 0){
            direccion.style="color:none; border-color:none";        
        }      
        else{
            direccion.style="color:green; border-color:green";
            direccion.blur()
        }
    }   
}
