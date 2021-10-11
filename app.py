import os
from flask import Flask, render_template,  request
from models import usuario
from forms import FormEditUsuario

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

""" @app.route('/template')
def hola_mundo():
    return render_template('template.html') """

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/registro/')
def registro():
    return render_template('registro.html')

@app.route('/gestioncomentario/')
def gestioncomentario():
    return render_template('gestion_comentario.html')

@app.route('/administrador/')
def administrador():
    formulario = FormEditUsuario()
    return render_template('administrador.html',lista_usuarios=usuario.listado(), formBuscar=formulario)

@app.route('/administrador/gestionar/EditNickname=<nickname>', methods=["GET", "POST"])
def edit_usuario(nickname):
    if request.method == "GET":
        formulario = FormEditUsuario()
        obj_mensaje =usuario.cargar(nickname)
        if obj_mensaje:
            formulario.nombre.data = obj_mensaje.nombre
            formulario.apellidos.data = obj_mensaje.apellidos
            formulario.correo.data = obj_mensaje.correo
            formulario.documento.data = obj_mensaje.documento
            formulario.celular.data = obj_mensaje.celular
            return render_template('administrador.html',usuario=obj_mensaje,lista_usuarios=usuario.listado(), opcion="editar", form=formulario)
        return render_template('administrador.html',error="Ocurrio un error")
    else:
        formulario = FormEditUsuario(request.form)
        if formulario.validate_on_submit():

            obj_mensaje = usuario.cargar(nickname)
            if obj_mensaje:
                obj_mensaje.nombre = formulario.nombre.data
                obj_mensaje.apellidos = formulario.apellidos.data
                obj_mensaje.correo = formulario.correo.data
                obj_mensaje.documento = formulario.documento.data
                obj_mensaje.celular = formulario.celular.data
                obj_mensaje.nickname = nickname
                obj_mensaje.editar(obj_mensaje.nombre, obj_mensaje.apellidos, obj_mensaje.correo, obj_mensaje.documento, obj_mensaje.celular, obj_mensaje.nickname)
                return render_template('administrador.html',usuario=obj_mensaje,lista_usuarios=usuario.listado(), opcion="editar",form=FormEditUsuario(), mensaje="Editado correctamente")

        return render_template('administrador.html',lista_usuarios=usuario.listado(), mensaje="Error en el proceso de editar usuario")


@app.route('/administrador/gestionar/GetNickname=<nickname>')
def get_usuario(nickname):
    obj_mensaje =usuario.cargar(nickname)
    if obj_mensaje:
        return render_template('administrador.html',usuario=obj_mensaje,lista_usuarios=usuario.listado(), opcion="editar",mensaje="Editado correctamente")
    return render_template('administrador.html',error="Ocurrio un error")

@app.route('/administrador/gestionar/DeleteNickname=<nickname>')
def delete_usuario(nickname):
    obj_mensaje =usuario.delete(nickname)
    if obj_mensaje:
        obj_mensaje+= nickname
        return render_template('administrador.html',mensaje=obj_mensaje,lista_usuarios=usuario.listado())
    return render_template('administrador.html',error="Ocurrio un error")

@app.route('/administrador/gestionar/BlockNickname=<nickname><estado>')
def block_usuario(nickname, estado):
    obj_mensaje =usuario.block(nickname, estado)
    if obj_mensaje:
        if estado == "T":
            obj_mensaje="Usuario "+ nickname+" bloqueado "
        elif estado == "F":
            obj_mensaje="Usuario "+ nickname+" desbloqueado "
        return render_template('administrador.html',mensaje=obj_mensaje,lista_usuarios=usuario.listado(), block=estado)
    return render_template('administrador.html',error="Ocurrio un error")


@app.route('/')
def index():
    return render_template('index.html')

"""Ruta para llamar a los productos de hombre"""
@app.route('/productos_hombre/')
def lista_de_productos_hombre():
    return render_template('productos_hombre.html')

"""Ruta para llamar a los productos de mujer"""
@app.route('/productos_mujer/')
def lista_de_productos_mujer():
    return render_template('productos_mujer.html')

"""Ruta para la gestión de perfil (Mi Cuenta)"""
@app.route('/gestion_micuenta/')
def gestion_micuenta():
    return render_template('gestion_micuenta.html')
