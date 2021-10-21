import os
from flask import Flask, render_template,  request, redirect, url_for
from models import *
from forms import *
from werkzeug.utils import redirect

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/')
def login():
    return render_template('login.html', form=FormLogin())

@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    if request.method=='GET':
        return render_template('registro.html', form=FormRegistro())
    else:
        #Formulario de ingreso para el método POST
        #Lo que el usuario escribió en Jinja lo trae para esta clase
        form_ingreso=FormRegistro(request.form)
        #Para validad los campos del formulario con el wtf
        if form_ingreso.validate_on_submit:
            #Se crea el objeto registro y se instancia en el orden del constructor, pero con el nombre del forms.py
            obj_registro=persona(form_ingreso.documento.data,form_ingreso.nickname.data,form_ingreso.nombre.data,form_ingreso.apellido.data,form_ingreso.correo.data,form_ingreso.telefono.data,form_ingreso.sexo.data,form_ingreso.direccion.data,form_ingreso.pais.data,form_ingreso.departamento.data,form_ingreso.ciudad.data,form_ingreso.contrasena.data,"user","T")
            if obj_registro.insertar_registro():
                return redirect(url_for('login'))
            return render_template('registro.html', form=FormRegistro(),error="Algo falló al intentar registrar sus datos, intente nuevamente")
        return render_template('registro.html', form=FormRegistro(),error="Todos los campos son requeridos, verifique los campos e intente nuevamente")
            
 

                
@app.route('/producto/')
def productoind():
    return render_template('ProductoIndividual.html')

@app.route('/carrito/')
def carrito():
    return render_template('Carrito.html')
@app.route('/gestioncomentario/')
def gestioncomentario():
    return render_template('gestion_comentario.html', form=FormGestionarComentario())

@app.route('/administrador/')
def administrador():
    if request.method == "POST":
        crear_usuario()
    return render_template('administrador.html',lista_usuarios=usuario.listado(), formBuscar=FormBuscar())

@app.route('/administrador/gestionar/EditNickname=<nickname>', methods=["GET", "POST"])
def edit_usuario(nickname):
    if request.method == "GET":
        formulario = FormCrearUsuario()
        obj_usuario =usuario.cargar(nickname)
        if obj_usuario:
            formulario.nombre.data = obj_usuario.nombre
            formulario.apellidos.data = obj_usuario.apellidos
            formulario.correo.data = obj_usuario.correo
            formulario.documento.data = obj_usuario.documento
            formulario.celular.data = obj_usuario.telefono
            formulario.sexo.data = obj_usuario.telefono
            return render_template('administrador.html',usuario=obj_usuario,lista_usuarios=usuario.listado(), opcion="Editar", form=formulario, formBuscar=FormBuscar())
        return render_template('administrador.html',error="No existe el usuario",lista_usuarios=usuario.listado(), formBuscar=FormBuscar())
    else:
        formulario = FormEditUsuario(request.form)
        if formulario.validate_on_submit():
            obj_usuario = usuario.cargar(nickname)
            if obj_usuario:
                obj_usuario.nombre = formulario.nombre.data
                obj_usuario.correo = formulario.correo.data
                obj_usuario.documento = formulario.documento.data
                obj_usuario.telefono = formulario.celular.data
                obj_usuario.sexo = formulario.sexo.data
                obj_usuario.editar(obj_usuario.nombre, obj_usuario.apellidos, obj_usuario.correo, obj_usuario.documento, obj_usuario.telefono, obj_usuario.nickname, obj_usuario.sexo)
                return render_template('administrador.html',usuario=obj_usuario,lista_usuarios=usuario.listado(), opcion="Editar",form=FormEditUsuario(), mensaje="Editado correctamente", formBuscar=FormBuscar())
        return render_template('administrador.html',lista_usuarios=usuario.listado(), error="Error en el proceso de editar usuario",form=FormEditUsuario(), formBuscar=FormBuscar())

@app.route('/administrador/gestionar/buscar', methods=["GET", "POST"])
def buscar_usuario():
    if request.method == "GET":
        formulario = FormCrearUsuario()
        form = FormBuscar
        return render_template('administrador.html',lista_usuarios=usuario.listado(), opcion="Editar", form=formulario, formBuscar=FormBuscar())
    else:
        form = FormBuscar(request.form)
        formulario = FormEditUsuario()
        if form.validate_on_submit() or formulario.validate_on_submit():
            obj_usuario = usuario.cargar(form.buscar.data)
            if obj_usuario:
                formulario.nombre.data = obj_usuario.nombre
                formulario.apellidos.data = obj_usuario.apellidos
                formulario.correo.data = obj_usuario.correo
                formulario.documento.data = obj_usuario.documento
                formulario.celular.data = obj_usuario.telefono
                formulario.sexo.data = obj_usuario.sexo
                return render_template('administrador.html',usuario=obj_usuario,lista_usuarios=usuario.listado(), opcion="Editar",form=formulario, formBuscar=FormBuscar())
            return render_template('administrador.html',lista_usuarios=usuario.listado(), error="No existe el usuario, puede crearlo",opcion="crear",form=FormCrearUsuario(), formBuscar=FormBuscar())
        return render_template('administrador.html',lista_usuarios=usuario.listado(), error="Error en el proceso de crear usuario",opcion="Editar",form=FormCrearUsuario(), formBuscar=FormBuscar())

@app.route('/administrador/gestionar/crear', methods=["GET", "POST"])
def crear_usuario():
    if request.method == "GET":
        formulario = FormCrearUsuario()
        return render_template('administrador.html',lista_usuarios=usuario.listado(), opcion="Crear", form=formulario, formBuscar=FormBuscar())
    else:
        formulario = FormCrearUsuario(request.form)
        if formulario.validate_on_submit():
            obj_usuario = usuario(formulario.nickname.data,"T",formulario.nombre.data,formulario.apellidos.data,formulario.documento.data,formulario.celular.data,formulario.sexo.data,formulario.correo.data)
            if (obj_usuario.crear(obj_usuario.nombre, obj_usuario.apellidos, obj_usuario.correo, obj_usuario.documento, obj_usuario.telefono, obj_usuario.nickname,obj_usuario.sexo)):
                return render_template('administrador.html',usuario=obj_usuario,lista_usuarios=usuario.listado(), opcion="Editar",form=FormEditUsuario(), mensaje="Creado correctamente el usuario "+ formulario.nickname.data, formBuscar=FormBuscar())

            return render_template('administrador.html',lista_usuarios=usuario.listado(), error="Error en el proceso de crear usuario",opcion="Editar",form=FormEditUsuario(), formBuscar=FormBuscar())
        return render_template('administrador.html',lista_usuarios=usuario.listado(), error="Error en el proceso de crear usuario",opcion="Editar",form=FormEditUsuario(), formBuscar=FormBuscar())


@app.route('/administrador/gestionar/DeleteNickname=<nickname>')
def delete_usuario(nickname):
    obj_usuario =usuario.delete(nickname)
    if obj_usuario:
        obj_usuario+= nickname
        return render_template('administrador.html',mensaje=obj_usuario,lista_usuarios=usuario.listado(), formBuscar=FormBuscar())
    return render_template('administrador.html',error="No se pudo eliminar al usuario "+nickname,lista_usuarios=usuario.listado(), formBuscar=FormBuscar())

@app.route('/administrador/gestionar/BlockNickname=<nickname><estado>')
def block_usuario(nickname, estado):
    obj_usuario =usuario.block(nickname, estado)
    if obj_usuario:
        if estado == "T":
            obj_usuario="Usuario "+ nickname+" bloqueado "
        elif estado == "F":
            obj_usuario="Usuario "+ nickname+" desbloqueado "
        return render_template('administrador.html',mensaje=obj_usuario,lista_usuarios=usuario.listado(), block=estado, formBuscar=FormBuscar())
    return render_template('administrador.html',error="No se pudo bloquear al usuario",lista_usuarios=usuario.listado(), formBuscar=FormBuscar())

"""Ruta para llamar a los productos de hombre"""
@app.route('/productos/hombre/')
def lista_de_productos_hombre():
    return render_template('productos_hombre.html')

"""Ruta para llamar a los productos de mujer"""
@app.route('/productos/mujer/')
def lista_de_productos_mujer():
    return render_template('productos_mujer.html')

@app.route('/gestion/productos/')
def gestion_productos():
    return render_template('gestion_productos.html',form=FormGestionProducto(), )

"""Ruta para la gestión de perfil (Mi Cuenta)"""
@app.route('/gestion/micuenta/')
def gestion_micuenta():
    return render_template('gestion_micuenta.html', form=FormMiCuenta())

"""Ruta para la gestión de Superadministrador"""
@app.route('/superadministrador/')
def superadministrador():
    return render_template('superadministrador.html', form=FormAdministrador(), formBuscar=FormBuscarAdministrador())

"""Ruta para todos los comentarios de un producto"""
@app.route('/comentarios/')
def todos_los_comentarios():
    return render_template('todos_los_comentarios.html')

@app.route('/contactos/')
def contactos():
    return render_template('contactos.html')

@app.route('/linkedinInri')
def linkedinInri():
    return redirect('https://www.linkedin.com/in/stivenas')

@app.route('/linkedinJulian')
def linkedinJulian():
    return redirect('https://www.linkedin.com/in/julianga/')

@app.route('/linkedinRau')
def linkedinRaul():
    return redirect('https://www.linkedin.com/in/raúl-andres-castaño-castellar-41b75bb3/')

@app.route('/linkedinDavid')
def linkedinDavid():
    return redirect('https://www.linkedin.com/in/david-daniel-hernandez-molina-98aab920a/')

@app.route('/linkedinMajo')
def linkedinMajo():
    return redirect('https://www.linkedin.com/in/mar%C3%ADa-jos%C3%A9-sierra-jim%C3%A9nez-3582a99a/')