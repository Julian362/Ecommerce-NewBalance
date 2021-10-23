import os
from flask import Flask, render_template,  request, redirect, url_for
from flask.wrappers import Request
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
    return render_template('login.html', form=FormGestionar())

@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    if request.method=='GET':
        return render_template('registro.html', form=FormGestionar())
    else:
        #Formulario de ingreso para el método POST
        #Lo que el usuario escribió en Jinja lo trae para esta clase
        form_ingreso=FormGestionar(request.form)
        #Para validad los campos del formulario con el wtf
        if form_ingreso.validate_on_submit:
            #Se crea el objeto registro y se instancia en el orden del constructor, pero con el nombre del forms.py
            obj_registro=persona(form_ingreso.documento.data,form_ingreso.nickname.data,form_ingreso.nombre.data,form_ingreso.apellido.data,form_ingreso.correo.data,form_ingreso.telefono.data,form_ingreso.sexo.data,form_ingreso.direccion.data,form_ingreso.pais.data,form_ingreso.departamento.data,form_ingreso.ciudad.data,form_ingreso.contrasena.data,"user","T")
            if obj_registro.insertar_registro():
                return redirect(url_for('login'))
            return render_template('registro.html', form=FormGestionar(), error="Algo falló al intentar registrar sus datos, intente nuevamente")
        return render_template('registro.html', form=FormGestionar(), error="Todos los campos son requeridos, verifique los campos e intente nuevamente")




@app.route('/producto/')
def productoind():
    return render_template('ProductoIndividual.html')

@app.route('/carrito/')
def carrito():
    return render_template('Carrito.html')

"""-----------------------------INICIO COMENTARIO-----------------------------"""


@app.route('/comentario/gestionar/crear/<referencia>-<puntuacion>-<documento>', methods=["GET", "POST"])
def crear_comentario(referencia,puntuacion,documento):
    if request.method == "GET":
        form=FormGestionarComentario()
        obj_calificacion = calificacion("",0,"",referencia,persona.cargar("user",documento).nickname,documento)
        return render_template('gestion_comentario.html', opcion="Crear", form=form, calificacionCrear = obj_calificacion)
    else:
        form=FormGestionarComentario(request.form)
        obj_calificacion = calificacion("",puntuacion,form.comentario.data,referencia,persona.cargar("user",documento).nickname,documento)
        if form.validate_on_submit():
            if obj_calificacion.crear():
                return redirect(url_for('editar_comentario',referencia=referencia,puntuacion=puntuacion,documento=documento))
            return render_template('gestion_comentario.html', opcion="Crear", form=form, calificacionCrear = obj_calificacion,error="No se pudo crear el comentario ")
        return render_template('gestion_comentario.html', opcion="Crear", form=form, calificacionCrear = obj_calificacion,error="No se pudo validar el crear el comentario ")


@app.route('/comentario/gestionar/editar/<referencia>-<puntuacion>-<documento>', methods=["GET", "POST"])
def editar_comentario(referencia,puntuacion,documento):

    if request.method == "GET":
        obj_calificacion=calificacion.cargar(documento,referencia)
        form=FormGestionarComentario()
        form.comentario.data = obj_calificacion.comentario
        return render_template('gestion_comentario.html', opcion="Editar", form=form, calificacion=obj_calificacion )
    else:
        form=FormGestionarComentario(request.form)
        obj_calificacion=calificacion.cargar(documento,referencia)
        obj_calificacion_validar=calificacion.editar(puntuacion,form.comentario.data,referencia,obj_calificacion.id)
        obj_calificacion=calificacion.cargar(documento,referencia)
        if obj_calificacion_validar:
            return render_template('gestion_comentario.html', form=FormGestionarComentario(), opcion="Editar",calificacion=obj_calificacion, mensaje="Editado correctamente")
        return render_template('gestion_comentario.html', form=FormGestionarComentario(), opcion="Crear", error="No se pudo editar el comentario")

@app.route('/comentario/gestionar/eliminar/<id>')
def delete_comentario(id):
    obj_calificacion =calificacion.delete(id)
    if obj_calificacion:
        obj_calificacion+= id
        return render_template('gestion_comentario.html', opcion="Crear", mensaje="Borrado correctamente")
    return render_template('gestion_comentario.html', form=FormGestionarComentario(), opcion="Crear", error="No se pudo editar el comentario")

"""-----------------------------FIN COMENTARIO-----------------------------"""


"""-----------------------------INICIO ADMINISTRADOR-----------------------------"""
@app.route('/administrador/')
def administrador():
    if request.method == "POST":
        crear_usuario()
    return render_template('administrador.html',lista_usuarios=persona.listado("user"), formBuscar=FormBuscar())

@app.route('/administrador/gestionar/Edit/<documento>', methods=["GET", "POST"])
def edit_usuario(documento):
    if request.method == "GET":
        formulario = FormGestionar()
        obj_usuario =persona.cargar("user",documento)
        if obj_usuario:
            formulario.documento.data = obj_usuario.documento
            formulario.nickname.data = obj_usuario.nickname
            formulario.nombre.data = obj_usuario.nombre
            formulario.apellidos.data = obj_usuario.apellidos
            formulario.correo.data = obj_usuario.correo
            formulario.telefono.data = obj_usuario.telefono
            formulario.sexo.data = obj_usuario.sexo
            formulario.direccion.data = obj_usuario.direccion
            formulario.pais.data = obj_usuario.pais
            formulario.departamento.data = obj_usuario.departamento
            formulario.ciudad.data = obj_usuario.ciudad
            formulario.contrasena.data = obj_usuario.contrasena
            return render_template('administrador.html',usuario=obj_usuario,lista_usuarios=persona.listado("user"), opcion="Editar", form=formulario, formBuscar=FormBuscar())
        return render_template('administrador.html',error="No existe el usuario",lista_usuarios=persona.listado("user"), formBuscar=FormBuscar())
    else:
        formulario = FormGestionar(request.form)
        if formulario.validate_on_submit():
            obj_usuario = persona.editar(formulario.documento.data,formulario.nickname.data,formulario.nombre.data,formulario.apellidos.data,formulario.correo.data,formulario.telefono.data,formulario.sexo.data,formulario.direccion.data,formulario.pais.data,formulario.departamento.data,formulario.ciudad.data,formulario.contrasena.data,"user")
            if obj_usuario:
                obj_usuario= obj_usuario =persona.cargar("user",documento)
                return render_template('administrador.html',usuario=obj_usuario,lista_usuarios=persona.listado("user"), opcion="Editar",form=FormGestionar(), mensaje="Editado correctamente", formBuscar=FormBuscar())
        return render_template('administrador.html',lista_usuarios=persona.listado("user"), error="Verifique los datos ingresados",form=FormGestionar(), formBuscar=FormBuscar())

@app.route('/administrador/gestionar/buscar', methods=["GET", "POST"])
def buscar_usuario():
    if request.method == "GET":
        return render_template('administrador.html',lista_usuarios=persona.listado("user"), opcion="Editar", form=FormGestionar(), formBuscar=FormBuscar())
    else:
        form = FormBuscar(request.form)
        formulario = FormGestionar()
        if form.validate_on_submit() or formulario.validate_on_submit():
            obj_usuario = persona.cargar("user",form.buscar.data)
            if obj_usuario:
                formulario.documento.data = obj_usuario.documento
                formulario.nickname.data = obj_usuario.nickname
                formulario.nombre.data = obj_usuario.nombre
                formulario.apellidos.data = obj_usuario.apellidos
                formulario.correo.data = obj_usuario.correo
                formulario.telefono.data = obj_usuario.telefono
                formulario.sexo.data = obj_usuario.sexo
                formulario.direccion.data = obj_usuario.direccion
                formulario.pais.data = obj_usuario.pais
                formulario.departamento.data = obj_usuario.departamento
                formulario.ciudad.data = obj_usuario.ciudad
                formulario.contrasena.data = obj_usuario.contrasena
                return render_template('administrador.html',usuario=obj_usuario,lista_usuarios=persona.listado("user"), opcion="Editar",form=formulario, formBuscar=FormBuscar())
            return render_template('administrador.html',lista_usuarios=persona.listado("user"), error="No existe el usuario, puede crearlo",opcion="crear",form=FormGestionar(), formBuscar=FormBuscar())
        return render_template('administrador.html',lista_usuarios=persona.listado("user"), error="Error en el proceso de buscar usuario",opcion="Crear",form=FormGestionar(), formBuscar=FormBuscar())

@app.route('/administrador/gestionar/crear', methods=["GET", "POST"])
def crear_usuario():
    if request.method == "GET":
        return render_template('administrador.html',lista_usuarios=persona.listado("user"), opcion="Crear", form=FormGestionar(), formBuscar=FormBuscar())
    else:
        formulario = FormGestionar(request.form)
        if formulario.validate_on_submit():
            obj_usuario = persona(formulario.documento.data, formulario.nickname.data,formulario.nombre.data, formulario.apellidos.data, formulario.correo.data, formulario.telefono.data, formulario.sexo.data, formulario.direccion.data, formulario.pais.data, formulario.departamento.data, formulario.ciudad.data, formulario.contrasena.data, "user", "T")
            if obj_usuario.crear():
                return render_template('administrador.html',usuario=obj_usuario,lista_usuarios=persona.listado("user"), opcion="Editar",form=FormGestionar(), mensaje="Creado correctamente el usuario "+ formulario.nickname.data, formBuscar=FormBuscar())
            return render_template('administrador.html',lista_usuarios=persona.listado("user"), error="El usuario on documento "+formulario.documento.data +" ya existe, o ingreso un campo erroneo",opcion="Editar",form=FormGestionar(), formBuscar=FormBuscar())
        return render_template('administrador.html',lista_usuarios=persona.listado("user"), error="Error en el proceso de crear usuario, valide los campos ingresados",opcion="Editar",form=FormGestionar(), formBuscar=FormBuscar())

@app.route('/administrador/gestionar/Delete/<documento>')
def delete_usuario(documento):
    obj_usuario =persona.delete("user",documento)
    if obj_usuario:
        obj_usuario+= documento
        return render_template('administrador.html',mensaje=obj_usuario,lista_usuarios=persona.listado("user"), formBuscar=FormBuscar())
    return render_template('administrador.html',error="No se pudo eliminar al usuario "+documento,lista_usuarios=persona.listado("user"), formBuscar=FormBuscar())

@app.route('/administrador/gestionar/Block/<documento><estado>')
def block_usuario(documento, estado):
    obj_usuario =persona.block(documento, estado)
    if obj_usuario:
        if estado == "T":
            obj_usuario="Usuario "+ documento+" bloqueado "
        elif estado == "F":
            obj_usuario="Usuario "+ documento+" desbloqueado "
        return render_template('administrador.html',mensaje=obj_usuario,lista_usuarios=persona.listado("user"), block=estado, formBuscar=FormBuscar())
    return render_template('administrador.html',error="No se pudo bloquear al usuario",lista_usuarios=persona.listado("user"), formBuscar=FormBuscar())


"""-----------------------------FIN ADMINISTRADOR-----------------------------"""

"""Ruta para llamar a los productos de hombre"""
@app.route('/productos/hombre/')
def lista_de_productos_hombre():
    return render_template('productos_hombre.html', lista_productos_totales=producto.listado_referencia())

"""Ruta para llamar a los productos de mujer"""
@app.route('/productos/mujer/')
def lista_de_productos_mujer():
    return render_template('productos_mujer.html')

@app.route('/productos/gestion/', methods=['GET', 'POST'])
def gestion_productos():
    return render_template('gestion_productos.html', lista_productos=producto.listado(), form=FormGestionProducto())

@app.route('/productos/gestion/edit/BlockProducto=<referencia><estado>')
def block_producto(referencia, estado):
    obj_proEstado =producto.block(referencia, estado)
    if obj_proEstado:
        if estado == "T":
            obj_proEstado="Producto con "+ referencia+" bloqueado "
        elif estado == "F":
            obj_proEstado="Producto con "+ referencia+" desbloqueado "
        return render_template('gestion_productos.html',mensaje=obj_proEstado,lista_productos=producto.listado(), block=estado)
    return render_template('gestion_productos.html',error="No se pudo bloquear al producto",lista_productos=producto.listado())

@app.route('/productos/gestion/crear', methods=["GET", "POST"])
def crear_producto():
    if request.method == "GET":
        formulario = FormGestionProducto()
        return render_template('gestion_productos.html',lista_productos=producto.listado(), opcion="Crear", form=formulario)
    else:
        formulario = FormGestionProducto(request.form)
        if formulario.validate_on_submit():
            obj_crearProducto = producto(formulario.nombre.data, formulario.referencia.data, formulario.talla.data, formulario.precio.data,formulario.cantidad.data,formulario.descuento.data,formulario.color.data, formulario.descripcion.data, formulario.sexo.data)
            if (obj_crearProducto.crear()):
                return render_template('gestion_productos.html',producto=obj_crearProducto,lista_productos=producto.listado(), opcion="Editar",form=FormGestionProducto(), mensaje="Creado correctamente el producto "+ formulario.nombre.data)

            return render_template('gestion_productos.html',lista_productos=producto.listado(), error="Error en el proceso de crear producto",opcion="Crear",form=FormGestionProducto())
        return render_template('gestion_productos.html',lista_productos=producto.listado(), error="Error en el proceso de crear usuario",opcion="Crear",form=FormGestionProducto())

"""Ruta para la gestión de perfil (Mi Cuenta)"""
@app.route('/gestion/micuenta/')
def gestion_micuenta():
    return render_template('gestion_micuenta.html', form=FormGestionar())

"""Ruta para la gestión de Superadministrador"""
@app.route('/superadministrador/')
def superadministrador():
    return render_template('superadministrador.html', formBuscar=FormBuscarAdministrador(), listaAdmin=gestionAdministrador.listado_administrador())

@app.route('/superadministrador/gestionar/<documento>',  methods=["GET", "POST"])
def edit_administrador(documento):
    if request.method == "GET":
        formulario = FormGestionar()
        obj_admin = gestionAdministrador.cargar_datos(documento)
        if obj_admin:
            formulario.nombre.data = obj_admin.nombre
            formulario.apellidos.data = obj_admin.apellido
            formulario.documento.data = obj_admin.documento
            formulario.sexo.data = obj_admin.sexo
            formulario.nickname.data = obj_admin.nickname
            formulario.telefono.data = obj_admin.telefono
            formulario.correo.data = obj_admin.correo
            formulario.pais.data = obj_admin.pais
            formulario.departamento.data = obj_admin.departamento
            formulario.ciudad.data = obj_admin.ciudad
            formulario.direccion.data = obj_admin.direccion
            formulario.contrasena.data = obj_admin.contrasena
            return render_template('superadministrador.html', datosAdministrador=obj_admin, form=formulario, formBuscar=FormBuscarAdministrador(), listaAdmin=gestionAdministrador.listado_administrador(), opcion="Editar")
        return render_template('superadministrador.html', error="No existe el usuario", formBuscar=FormBuscarAdministrador(), listaAdmin=gestionAdministrador.listado_administrador())
    else:
        formulario = FormGestionar(request.form)
        if formulario.validate_on_submit():
            obj_admin = gestionAdministrador.cargar_datos(documento)
            if obj_admin:
                obj_admin.nombre = formulario.nombre.data
                obj_admin.apellido = formulario.apellidos.data
                obj_admin.documento = formulario.documento.data
                obj_admin.sexo = formulario.sexo.data
                obj_admin.nickname = formulario.nickname.data
                obj_admin.telefono = formulario.telefono.data
                obj_admin.correo = formulario.correo.data
                obj_admin.pais = formulario.pais.data
                obj_admin.departamento = formulario.departamento.data
                obj_admin.ciudad = formulario.ciudad.data
                obj_admin.direccion = formulario.direccion.data 
                obj_admin.contrasena = formulario.contrasena.data
                obj_admin.editar_datos()
                return render_template('superadministrador.html', datosAdministrador=obj_admin, formBuscar=FormBuscarAdministrador(), listaAdmin=gestionAdministrador.listado_administrador(), mensaje = "Se han editados los datos del administrador {0} correctamente".format(formulario.documento.data), opcion="Editar")
        return render_template('superadministrador.html', form=FormGestionar(), formBuscar=FormBuscarAdministrador(), listaAdmin=gestionAdministrador.listado_administrador(), error="Error en el proceso de editar usuario")

@app.route('/superadministrador/crear/', methods=["GET", "POST"])
def crear_administrador():
    if request.method == "GET":
        formulario = FormGestionar()
        return render_template('superadministrador.html', form = formulario, listaAdmin=gestionAdministrador.listado_administrador(), formBuscar=FormBuscarAdministrador(), opcion="Crear")
    else:
        formulario = FormGestionar(request.form)
        if formulario.validate_on_submit():
            obj_admin = gestionAdministrador(formulario.nombre.data, formulario.apellido.data, formulario.documento.data, formulario.sexo.data, formulario.nickname.data, formulario.telefono.data, formulario.correo.data, formulario.pais.data, formulario.departamento.data, formulario.ciudad.data, formulario.direccion.data, formulario.contrasena.data, "admin", "T")
            if (obj_admin.crear_admin()):
                return render_template('superadministrador.html', mensaje="Se ha creado correctamente el administrador {0}".format(formulario.documento.data), listaAdmin=gestionAdministrador.listado_administrador(), formBuscar=FormBuscarAdministrador(), opcion="Crear")
        return render_template('superadministrador.html', error="Error en el proceso de creación de administración",form=FormGestionar(), listaAdmin=gestionAdministrador.listado_administrador(), formBuscar=FormBuscarAdministrador(), opcion="Crear")
    

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