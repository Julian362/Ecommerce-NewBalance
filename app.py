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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/registro/')
def registro():
    return render_template('registro.html')

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
    formulario = FormEditUsuario()
    return render_template('administrador.html',lista_usuarios=usuario.listado(), formBuscar=formulario)

# ruta para editar usuarios por parte del administrador, acepta GET Y POST Y recibe el nickname del usuario a editar
@app.route('/administrador/gestionar/EditNickname=<nickname>', methods=["GET", "POST"])
def edit_usuario(nickname):
    # si el metodo  es GET entra al if
    if request.method == "GET":
        # se instancia el formulario de forms.py
        formulario = FormEditUsuario()
        # se  llama al cargar que cargar en base al nickname (primary key de la tabala usuario) y trae todos sus datos
        obj_mensaje =usuario.cargar(nickname)
        # si  si existe el objeto, osea si el usuario si existe
        if obj_mensaje:
            # al formulario le doy todos los valores que traje de la base de datos y que estan en el objeto obj_mensaje
            formulario.nombre.data = obj_mensaje.nombre
            formulario.apellidos.data = obj_mensaje.apellidos
            formulario.correo.data = obj_mensaje.correo
            formulario.documento.data = obj_mensaje.documento
            formulario.celular.data = obj_mensaje.celular
            # retorno el admniistrador.html, con el usuario, el listado de usuario, la opcion que es editar, y le envio el formulario ya editado
            return render_template('administrador.html',usuario=obj_mensaje,lista_usuarios=usuario.listado(), opcion="Editar", form=formulario)
        # si el objeto obj_mensaje no tiene nada se le manda un error al administrador.html
        return render_template('administrador.html',error="No existe el usuario",lista_usuarios=usuario.listado())
    # si el metodo no es GEt, es POST
    else:
        # Si es es POST trae todo lo que tiene el formulario, osea lo que esta en los input
        formulario = FormEditUsuario(request.form)
        # se valida que tenga el mismo token CSRF
        if formulario.validate_on_submit():
            # si ya se valido el token, se carga al usuario que esta en la base de datos y se guarda en obj_mensaje
            obj_mensaje = usuario.cargar(nickname)
            # si devuelve un objeto si existente entra al if
            if obj_mensaje:
                # se carga al obj_mensaje que es un usuario todos los atributos del formulario osea lo que esta en los input se trae para aca
                obj_mensaje.nombre = formulario.nombre.data
                obj_mensaje.apellidos = formulario.apellidos.data
                obj_mensaje.correo = formulario.correo.data
                obj_mensaje.documento = formulario.documento.data
                obj_mensaje.celular = formulario.celular.data
                obj_mensaje.nickname = nickname
                # llamo al editar y le mando todos los atributos que traje de el formulario, el cual ejecuta el update para la bd
                obj_mensaje.editar(obj_mensaje.nombre, obj_mensaje.apellidos, obj_mensaje.correo, obj_mensaje.documento, obj_mensaje.celular, obj_mensaje.nickname)
                # retorno el administrador.html y le mando el usuario,, la lista de usuarios, la opcion por si quiere seguir editando, el formulario para que cargue los input y tambien le mando el mensaje 
                return render_template('administrador.html',usuario=obj_mensaje,lista_usuarios=usuario.listado(), opcion="Editar",form=FormEditUsuario(), mensaje="Editado correctamente")
        # si  el validate_on_submit no es verificado osea el token es incorrecto le mando el listado de usuarios, el formulario, la lisatd e usuarios y un error
        return render_template('administrador.html',lista_usuarios=usuario.listado(), error="Error en el proceso de editar usuario",form=FormEditUsuario())

# ruta para crear usuarios por parte del administrador, acepta GET Y POST
@app.route('/administrador/gestionar/crear', methods=["GET", "POST"])
def crear_usuario():
    # si el metodo  es GET entra al if
    if request.method == "GET":
        # se instancia el formulario de forms.py
        formulario = FormEditUsuario()
        # retorno el admniistrador.html, con el usuario, el listado de usuario, la opcion que es editar, y le envio el formulario ya editado
        return render_template('administrador.html',lista_usuarios=usuario.listado(), opcion="Crear", form=formulario)
    # si el metodo no es GEt, es POST
    else:
        # Si es es POST trae todo lo que tiene el formulario, osea lo que esta en los input
        formulario = FormEditUsuario(request.form)
        # se valida que tenga el mismo token CSRF
        if formulario.validate_on_submit():
            # si ya se valido el token, se carga al usuario que esta en la base de datos y se guarda en obj_mensaje
            obj_mensaje = usuario()
            # se carga al obj_mensaje que es un usuario todos los atributos del formulario osea lo que esta en los input se trae para aca
            obj_mensaje.nombre = formulario.nombre.data
            obj_mensaje.apellidos = formulario.apellidos.data
            obj_mensaje.correo = formulario.correo.data
            obj_mensaje.documento = formulario.documento.data
            obj_mensaje.celular = formulario.celular.data
            obj_mensaje.nickname = formulario.nickname.data
            obj_mensaje.sexo = "M"
            # llamo al crear y le mando todos los atributos que traje de el formulario, el cual ejecuta el update para la bd
            if (obj_mensaje.crear(obj_mensaje.nombre, obj_mensaje.apellidos, obj_mensaje.correo, obj_mensaje.documento, obj_mensaje.celular, obj_mensaje.nickname)):
                # retorno el administrador.html y le mando el usuario,, la lista de usuarios, la opcion por si quiere seguir editando, el formulario para que cargue los input y tambien le mando el mensaje
                return render_template('administrador.html',usuario=obj_mensaje,lista_usuarios=usuario.listado(), opcion="Editar",form=FormEditUsuario(), mensaje="Editado correctamente")

            return render_template('administrador.html',lista_usuarios=usuario.listado(), error="Error en el proceso de crear usuario",form=FormEditUsuario())
        # si  el validate_on_submit no es verificado osea el token es incorrecto le mando el listado de usuarios, el formulario, la lisatd e usuarios y un error
        return render_template('administrador.html',lista_usuarios=usuario.listado(), error="Error en el proceso de crear usuario",form=FormEditUsuario())


# @app.route('/administrador/gestionar/GetNickname=<nickname>')
# def get_usuario(nickname):
#     obj_mensaje =usuario.cargar(nickname)
#     if obj_mensaje:
#         return render_template('administrador.html',usuario=obj_mensaje,lista_usuarios=usuario.listado(), opcion="editar",mensaje="Editado correctamente")
#     return render_template('administrador.html',error="El usuario no existe")

# ruta para borrar al usuario
@app.route('/administrador/gestionar/DeleteNickname=<nickname>')
def delete_usuario(nickname):
    # llama al delete de la clase usuario que ejecuta el delete sql
    obj_mensaje =usuario.delete(nickname)
    # si responde algo, osea el objeto exite entra al if, que en este caso devuelve un String
    if obj_mensaje:
        # le concateno al string que me llego el nickname del usuario
        obj_mensaje+= nickname
        # le mando al administrador.html el mensaje y la lista de usuarios
        return render_template('administrador.html',mensaje=obj_mensaje,lista_usuarios=usuario.listado())
    # si no borro al usuario se le mando un error con el nickname, y la lista de usuarios
    return render_template('administrador.html',error="No se pudo eliminar al usuario "+nickname,lista_usuarios=usuario.listado())

# ruta para bloquear al usuario, que recibe el usuaruio y el esatdo, si esta bloqeuado se desbloquea o viceversa
@app.route('/administrador/gestionar/BlockNickname=<nickname><estado>')
def block_usuario(nickname, estado):
    # se llama a la funcion block que ejecuta un update actualizando en la base de datos el estado
    obj_mensaje =usuario.block(nickname, estado)
    # si obj_mensaje = true entra al if
    if obj_mensaje:
        # si el estado que llego es T osea true es que el usuario paso de desbloqueado a bloqueado
        if estado == "T":
            obj_mensaje="Usuario "+ nickname+" bloqueado "
        # si el estado que llego es F osea false es que el usuario paso de loqueado a desbloqueado
        elif estado == "F":
            obj_mensaje="Usuario "+ nickname+" desbloqueado "
        # se retorna al usuario el mensaje de si fue desbloqueado o bloqeuaqdo, la lista de ususario y el block para que cambie el color en el administrador.html
        return render_template('administrador.html',mensaje=obj_mensaje,lista_usuarios=usuario.listado(), block=estado)
    # si retorna falso es que no pudo bloquear al usuario asi que se le manda ese error y el listado de usaurios
    return render_template('administrador.html',error="No se pudo bloquear al usuario",lista_usuarios=usuario.listado())

"""Ruta para llamar a los productos de hombre"""
@app.route('/productos/hombre/')
def lista_de_productos_hombre():
    return render_template('productos_hombre.html')

"""Ruta para llamar a los productos de mujer"""
@app.route('/productos/mujer/')
def lista_de_productos_mujer():
    return render_template('productos_mujer.html')

@app.route('/gestion_productos/')
def gestion_productos():
    return render_template('gestion_productos.html')

"""Ruta para la gestión de perfil (Mi Cuenta)"""
@app.route('/gestion/micuenta/')
def gestion_micuenta():
    return render_template('gestion_micuenta.html')

"""Ruta para la gestión de Superadministrador"""
@app.route('/superadministrador/')
def superadministrador():
    return render_template('superadministrador.html')

"""Ruta para todos los comentarios de un producto"""
@app.route('/comentarios/')
def todos_los_comentarios():
    return render_template('todos_los_comentarios.html')

@app.route('/contactos/')
def contactos():
    return render_template('contactos.html')
