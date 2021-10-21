import os
from flask import Flask, render_template,  request, redirect
from models import usuario
from forms import FormEditUsuario, FormCrearUsuario, FormBuscar, FormRegistro, FormMiCuenta, FormAdministrador, FormBuscarAdministrador

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/registro/')
def registro():
    return render_template('registro.html', form=FormRegistro())

@app.route('/producto/')
def productoind():
    return render_template('ProductoIndividual.html')

@app.route('/carrito/')
def carrito():
    return render_template('Carrito.html')
@app.route('/gestioncomentario/')
def gestioncomentario():
    return render_template('gestion_comentario.html')

@app.route('/administrador/')
def administrador():
    if request.method == "POST":
        crear_usuario()
    return render_template('administrador.html',lista_usuarios=usuario.listado(), formBuscar=FormBuscar())

@app.route('/administrador/gestionar/EditNickname=<nickname>', methods=["GET", "POST"])
def edit_usuario(nickname):
    if request.method == "GET":
        formulario = FormCrearUsuario()
        obj_mensaje =usuario.cargar(nickname)
        if obj_mensaje:
            formulario.nombre.data = obj_mensaje.nombre
            formulario.apellidos.data = obj_mensaje.apellidos
            formulario.correo.data = obj_mensaje.correo
            formulario.documento.data = obj_mensaje.documento
            formulario.celular.data = obj_mensaje.telefono
            formulario.sexo.data = obj_mensaje.telefono
            return render_template('administrador.html',usuario=obj_mensaje,lista_usuarios=usuario.listado(), opcion="Editar", form=formulario, formBuscar=FormBuscar())
        return render_template('administrador.html',error="No existe el usuario",lista_usuarios=usuario.listado(), formBuscar=FormBuscar())
    else:
        formulario = FormEditUsuario(request.form)
        if formulario.validate_on_submit():
            obj_mensaje = usuario.cargar(nickname)
            if obj_mensaje:
                obj_mensaje.nombre = formulario.nombre.data
                obj_mensaje.correo = formulario.correo.data
                obj_mensaje.documento = formulario.documento.data
                obj_mensaje.telefono = formulario.celular.data
                obj_mensaje.sexo = formulario.sexo.data
                obj_mensaje.editar(obj_mensaje.nombre, obj_mensaje.apellidos, obj_mensaje.correo, obj_mensaje.documento, obj_mensaje.telefono, obj_mensaje.nickname, obj_mensaje.sexo)
                return render_template('administrador.html',usuario=obj_mensaje,lista_usuarios=usuario.listado(), opcion="Editar",form=FormEditUsuario(), mensaje="Editado correctamente", formBuscar=FormBuscar())
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
            obj_mensaje = usuario.cargar(form.buscar.data)
            if obj_mensaje:
                formulario.nombre.data = obj_mensaje.nombre
                formulario.apellidos.data = obj_mensaje.apellidos
                formulario.correo.data = obj_mensaje.correo
                formulario.documento.data = obj_mensaje.documento
                formulario.celular.data = obj_mensaje.telefono
                formulario.sexo.data = obj_mensaje.sexo
                return render_template('administrador.html',usuario=obj_mensaje,lista_usuarios=usuario.listado(), opcion="Editar",form=formulario, formBuscar=FormBuscar())
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
            obj_mensaje = usuario(formulario.nickname.data,"T",formulario.nombre.data,formulario.apellidos.data,formulario.documento.data,formulario.celular.data,formulario.sexo.data,formulario.correo.data)
            if (obj_mensaje.crear(obj_mensaje.nombre, obj_mensaje.apellidos, obj_mensaje.correo, obj_mensaje.documento, obj_mensaje.telefono, obj_mensaje.nickname,obj_mensaje.sexo)):
                return render_template('administrador.html',usuario=obj_mensaje,lista_usuarios=usuario.listado(), opcion="Editar",form=FormEditUsuario(), mensaje="Creado correctamente el usuario "+ formulario.nickname.data, formBuscar=FormBuscar())

            return render_template('administrador.html',lista_usuarios=usuario.listado(), error="Error en el proceso de crear usuario",opcion="Editar",form=FormEditUsuario(), formBuscar=FormBuscar())
        return render_template('administrador.html',lista_usuarios=usuario.listado(), error="Error en el proceso de crear usuario",opcion="Editar",form=FormEditUsuario(), formBuscar=FormBuscar())


@app.route('/administrador/gestionar/DeleteNickname=<nickname>')
def delete_usuario(nickname):
    obj_mensaje =usuario.delete(nickname)
    if obj_mensaje:
        obj_mensaje+= nickname
        return render_template('administrador.html',mensaje=obj_mensaje,lista_usuarios=usuario.listado(), formBuscar=FormBuscar())
    return render_template('administrador.html',error="No se pudo eliminar al usuario "+nickname,lista_usuarios=usuario.listado(), formBuscar=FormBuscar())

@app.route('/administrador/gestionar/BlockNickname=<nickname><estado>')
def block_usuario(nickname, estado):
    obj_mensaje =usuario.block(nickname, estado)
    if obj_mensaje:
        if estado == "T":
            obj_mensaje="Usuario "+ nickname+" bloqueado "
        elif estado == "F":
            obj_mensaje="Usuario "+ nickname+" desbloqueado "
        return render_template('administrador.html',mensaje=obj_mensaje,lista_usuarios=usuario.listado(), block=estado, formBuscar=FormBuscar())
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
    return render_template('gestion_productos.html')

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