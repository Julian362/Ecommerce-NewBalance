import os
import functools
from flask import Flask, render_template,  request, redirect, url_for, request,g,url_for,session
from flask.wrappers import Request
from models import *
from forms import *
from werkzeug.utils import redirect

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html', lista_productosSer=producto.listado_searchs())


# --------------------LOGIN-----------------------------
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.usuario is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.before_request
def cargar_usuario_autenticado():
    user_correo=session.get('user_correo')
    if user_correo is None:
        g.user=None
    else:
        g.user=usuario.cargar(user_correo)




@app.route('/login/', methods=("GET", "POST"))
def login():
    if request.method == "GET":
        return render_template("login.html",form=FormGestionar(), lista_productosSer=producto.listado_searchs())
    else:
        formulario=FormGestionar(request.form)
        # obj_usuario = persona(formulario.correo.data,formulario.contrasena.data)
        # obj_usuario = persona('','','','',request.form['correo'],'','','','','','',request.form['contrasena'],'','',)
        obj_usuario = usuario('','',formulario.correo.data, formulario.contrasena.data,'')
        if not obj_usuario.correo.__contains__("'") and not obj_usuario.contrasena.__contains__("'"):
            if obj_usuario.logear():
                session.clear()
                session['user_correo'] = obj_usuario.correo
                return redirect('/')
                # return redirect(url_for('get_/'))
        return render_template('login.html', error="Usuario o contraseña invalido",form=FormGestionar(), lista_productosSer=producto.listado_searchs())

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ----------------------------------------------------------------------------


# -------------------------REGISTRO-------------------------------------------------

@app.route('/registro/', methods=['GET', 'POST'])
def registro():
    if request.method=='GET':
        return render_template('registro.html', form=FormGestionar(), lista_productosSer=producto.listado_searchs())
    else:
        #Formulario de ingreso para el método POST
        #Lo que el usuario escribió en Jinja lo trae para esta clase
        form_ingreso=FormGestionar(request.form)
        #Para validad los campos del formulario con el wtf
        if form_ingreso.validate_on_submit:
            #Se crea el objeto registro y se instancia en el orden del constructor, pero con el nombre del forms.py
            obj_registro=persona(form_ingreso.documento.data,form_ingreso.nickname.data,form_ingreso.nombre.data,form_ingreso.apellidos.data,form_ingreso.correo.data,form_ingreso.telefono.data,form_ingreso.sexo.data,form_ingreso.direccion.data,form_ingreso.pais.data,form_ingreso.departamento.data,form_ingreso.ciudad.data,form_ingreso.contrasena.data,"user","T")
            if obj_registro.insertar_registro():
                return redirect(url_for('login'))
            return render_template('registro.html', form=FormGestionar(), error="Algo falló al intentar registrar sus datos, intente nuevamente", lista_productosSer=producto.listado_searchs())
        return render_template('registro.html', form=FormGestionar(), error="Todos los campos son requeridos, verifique los campos e intente nuevamente", lista_productosSer=producto.listado_searchs())
# ----------------------------------------------------------------------------


#codigo David
@app.route('/producto/<referencia>')
def productoind(referencia):    
    promedio=0
    acumulador=0
    lista_califiacion=calificacion.todos_los_comentarios(referencia)
    for i in lista_califiacion:
        acumulador+=i['puntuacion']
    if len(lista_califiacion)>0:
        promedio=acumulador/len(lista_califiacion)
    return render_template('Producto_individual.html', Producto_Referencia=producto.productoindividual(referencia), item=producto.cargarProducto(referencia), form=FormFiltrarProductoIndividual(),lista_comentarios=calificacion.todos_los_comentarios(referencia),promedio=promedio, promedio_comentarios=calificacion.promedio_comentarios(referencia), tres_registros=calificacion.tres_comentarios(referencia), filtro=FormFiltrarProducto())

@app.route('/carrito/<documento>')
def carrito(documento):
    Lista_Carrito=producto.cargar_carrito(documento)
    total = 0
    for i in Lista_Carrito:
        total += i["precio"]
    return render_template('Carrito.html', Lista_Carrito=Lista_Carrito, total=total, filtro=FormFiltrarProducto())

@app.route('/<documento>-<referencia>',methods=["POST"])
def agregar_carrito(documento,referencia):
    if request.method == "POST":
        form = FormFiltrarProducto(request.form)
        if producto.crear_carrito(referencia,documento,form.talla.data,form.color.data):
            return redirect(url_for('productoind',referencia=referencia))
        return redirect(url_for('productoind',referencia=referencia))

@app.route('/<id>--<documento>',methods=["POST"])
def borrar_producto_carrito(id,documento):
    if request.method == "POST":
        producto.borrar_carrito(id)
        return redirect(url_for('carrito',documento=documento))

"""-----------------------------INICIO COMENTARIO-----------------------------"""

@app.route('/comentario/gestionar/crear/<referencia>-<puntuacion>-<documento>', methods=["GET", "POST"])
def crear_comentario(referencia,puntuacion,documento):
    if request.method == "GET":
        form=FormGestionarComentario()
        obj_calificacion = calificacion("",0,"",referencia,persona.cargar("user",documento).nickname,documento)
        return render_template('gestion_comentario.html', opcion="Crear", form=form, calificacionCrear = obj_calificacion, lista_productosSer=producto.listado_searchs())
    else:
        form=FormGestionarComentario(request.form)
        obj_calificacion = calificacion("",puntuacion,form.comentario.data,referencia,persona.cargar("user",documento).nickname,documento)
        if form.validate_on_submit():
            if obj_calificacion.crear():
                return redirect(url_for('productoind',referencia=referencia))
            return render_template('gestion_comentario.html', opcion="Crear", form=form, calificacionCrear = obj_calificacion,error="No se pudo crear el comentario ")
        return render_template('gestion_comentario.html', opcion="Crear", form=form, calificacionCrear = obj_calificacion,error="No se pudo validar el crear el comentario ")


@app.route('/comentario/gestionar/editar/<referencia>-<puntuacion>-<documento>', methods=["GET", "POST"])
def editar_comentario(referencia,puntuacion,documento):

    if request.method == "GET":
        obj_calificacion=calificacion.cargar(documento,referencia)
        form=FormGestionarComentario()
        form.comentario.data = obj_calificacion.comentario
        return render_template('gestion_comentario.html', opcion="Editar", form=form, calificacion=obj_calificacion, lista_productosSer=producto.listado_searchs() )
    else:
        form=FormGestionarComentario(request.form)
        obj_calificacion=calificacion.cargar(documento,referencia)
        obj_calificacion_validar=calificacion.editar(puntuacion,form.comentario.data,referencia,obj_calificacion.id)
        obj_calificacion=calificacion.cargar(documento,referencia)
        if obj_calificacion_validar:
            return render_template('gestion_comentario.html', form=FormGestionarComentario(), opcion="Editar",calificacion=obj_calificacion, mensaje="Editado correctamente", lista_productosSer=producto.listado_searchs())
        return render_template('gestion_comentario.html', form=FormGestionarComentario(), opcion="Crear", error="No se pudo editar el comentario", lista_productosSer=producto.listado_searchs())

@app.route('/comentario/gestionar/eliminar/<id>')
def delete_comentario(id):
    obj_calificacion =calificacion.delete(id)
    if obj_calificacion:
        obj_calificacion+= id
        return render_template('gestion_comentario.html', opcion="Crear", mensaje="Borrado correctamente", lista_productos=producto.listado_searchs())
    return render_template('gestion_comentario.html', form=FormGestionarComentario(), opcion="Crear", error="No se pudo editar el comentario", lista_productosSer=producto.listado_searchs())

"""-----------------------------FIN COMENTARIO-----------------------------"""


"""-----------------------------INICIO ADMINISTRADOR-----------------------------"""
@app.route('/administrador/')
def administrador():
    if request.method == "POST":
        crear_usuario()
    return render_template('administrador.html',lista_usuarios=persona.listado("user"), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())

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
            formulario.contrasena.data = ""
            return render_template('administrador.html',usuario=obj_usuario,lista_usuarios=persona.listado("user"), opcion="Editar", form=formulario, formBuscar=FormBuscar(), lista_productos=producto.listado_searchs())
        return render_template('administrador.html',error="No existe el usuario",lista_usuarios=persona.listado("user"), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
    else:
        formulario = FormGestionar(request.form)
        if formulario.validate_on_submit():
            obj_usuario = persona.editar(documento,formulario.nickname.data,formulario.nombre.data,formulario.apellidos.data,formulario.correo.data,formulario.telefono.data,formulario.sexo.data,formulario.direccion.data,formulario.pais.data,formulario.departamento.data,formulario.ciudad.data,formulario.contrasena.data,"user")
            if obj_usuario:
                obj_usuario= obj_usuario =persona.cargar("user",documento)
                return render_template('administrador.html',usuario=obj_usuario,lista_usuarios=persona.listado("user"), opcion="Editar",form=FormGestionar(), mensaje="Se han editado los datos del ususario {0} {1} correctamente".format(formulario.nombre.data, formulario.apellidos.data), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
        return render_template('administrador.html',lista_usuarios=persona.listado("user"), error="Verifique los datos ingresados",form=FormGestionar(), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())

@app.route('/administrador/gestionar/buscar', methods=["GET", "POST"])
def buscar_usuario():
    if request.method == "GET":
        return render_template('administrador.html',lista_usuarios=persona.listado("user"), opcion="Editar", form=FormGestionar(), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
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
                return render_template('administrador.html',usuario=obj_usuario,lista_usuarios=persona.listado("user"), opcion="Editar",form=formulario, formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
            return render_template('administrador.html',lista_usuarios=persona.listado("user"), error="No existe el usuario, puede crearlo", opcion="crear",form=FormGestionar(), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
        return render_template('administrador.html',lista_usuarios=persona.listado("user"), error="Error en el proceso de buscar usuario",opcion="Crear",form=FormGestionar(), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())

@app.route('/administrador/gestionar/crear', methods=["GET", "POST"])
def crear_usuario():
    if request.method == "GET":
        return render_template('administrador.html',lista_usuarios=persona.listado("user"), opcion="Crear", form=FormGestionar(), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
    else:
        formulario = FormGestionar(request.form)
        if formulario.validate_on_submit():
            obj_usuario = persona(formulario.documento.data, formulario.nickname.data,formulario.nombre.data, formulario.apellidos.data, formulario.correo.data, formulario.telefono.data, formulario.sexo.data, formulario.direccion.data, formulario.pais.data, formulario.departamento.data, formulario.ciudad.data, formulario.contrasena.data, "user", "T")
            if obj_usuario.crear():
                return render_template('administrador.html',usuario=obj_usuario,lista_usuarios=persona.listado("user"), opcion="Editar",form=FormGestionar(), mensaje="Creado correctamente el usuario "+ formulario.nickname.data, formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
            return render_template('administrador.html',lista_usuarios=persona.listado("user"), error="El usuario con documento "+formulario.documento.data +" ya existe, o ingresó un campo erroneo",opcion="Editar",form=FormGestionar(), formBuscar=FormBuscar(), lista_produlista_productosSerctos=producto.listado_searchs())
        return render_template('administrador.html',lista_usuarios=persona.listado("user"), error="Error en el proceso de crear usuario, valide los campos ingresados",opcion="Editar",form=FormGestionar(), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())

@app.route('/administrador/gestionar/Delete/<documento>')
def delete_usuario(documento):
    obj_usuario =persona.delete("user",documento)
    if obj_usuario:
        obj_usuario+= documento
        return render_template('administrador.html',mensaje=obj_usuario,lista_usuarios=persona.listado("user"), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
    return render_template('administrador.html',error="No se pudo eliminar al usuario "+documento,lista_usuarios=persona.listado("user"), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())

@app.route('/administrador/gestionar/Block/<documento><estado>')
def block_usuario(documento, estado):
    obj_usuario =persona.block(documento, estado)
    if obj_usuario:
        if estado == "T":
            obj_usuario="Usuario "+ documento+" bloqueado "
        elif estado == "F":
            obj_usuario="Usuario "+ documento+" desbloqueado "
        return render_template('administrador.html',mensaje=obj_usuario,lista_usuarios=persona.listado("user"), block=estado, formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
    return render_template('administrador.html',error="No se pudo bloquear al usuario",lista_usuarios=persona.listado("user"), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())


"""-----------------------------FIN ADMINISTRADOR-----------------------------"""

""" -----------------------------INICIO PRODUCTOS-----------------------------"""

"""Ruta para llamar a los productos de hombre"""
@app.route('/productos/<sexo>/')
def lista_de_productos(sexo):
    #Variable para obtener el sexo de la base de datos por la letra M = Masculino y F = Femenino 
    s=""
    if sexo=="HOMBRE":
        s="M"
    if sexo=="MUJER":
        s="F"
    return render_template('productos.html', lista_productos_totales=producto.listado_referencia(s),sexo=sexo,filtro=FormFiltrarProducto(), lista_productosSer=producto.listado_searchs())
    
@app.route('/productos/<sexo>/filtros/', methods=["GET", "POST"])
def filtros_producto(sexo):
    s=""
    if sexo=="HOMBRE":
        s="M"
    if sexo=="MUJER":
        s="F"
    if request.method=="GET":
        return render_template('productos.html', lista_productos_totales=producto.listado_referencia(s),sexo=sexo,filtro=FormFiltrarProducto(), lista_productosSer=producto.listado_searchs())
        #Método POST
    else:
        formulario=FormFiltrarProducto(request.form)
        if formulario.validate_on_submit():
            if len(producto.filtrar(s, formulario.orden.data, formulario.talla.data, formulario.color.data))>0:
                return render_template('productos.html', lista_productos_totales=producto.filtrar(s, formulario.orden.data, formulario.talla.data, formulario.color.data),sexo=sexo,filtro=FormFiltrarProducto(), lista_productosSer=producto.listado_searchs())
            return render_template('productos.html', lista_productos_totales=producto.listado_referencia(s),sexo=sexo,filtro=FormFiltrarProducto(),  error="No hay productos asociados a los filtros requeridos", lista_productosSer=producto.listado_searchs())

        return render_template('productos.html', lista_productos_totales=producto.listado_referencia(s),sexo=sexo,filtro=FormFiltrarProducto(),  error="No hay productos asociados a los filtros requeridos", lista_productosSer=producto.listado_searchs())

# -------------------------------------GESTION PRODUCTOS---------------------------------------------------------
# Cambia de estado bloqueo STIVEN
@app.route('/productos/gestion/', methods=['GET', 'POST'])
def gestion_productos():
    return render_template('gestion_productos.html', lista_productos=producto.listado(),formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())

# Busca el id del producto en lista
@app.route('/productos/gestion/buscar', methods=["GET", "POST"])
def buscar_gestionproductos():
    if request.method == "GET":
        return render_template('gestion_productos.html',lista_productos=producto.listado(), opcion="Editar", form=FormGestionProducto(), formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
    else:
        form = FormBuscar(request.form)
        if form.validate_on_submit():
            obj_producto = producto.listado_buscarp(form.buscar.data)
            if obj_producto:
                return render_template('gestion_productos.html',lista_productos=obj_producto,  formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
            return render_template('gestion_productos.html',lista_productos=producto.listado(), error="No existe el producto, puede crearlo", formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
        return render_template('gestion_productos.html',lista_productos=producto.listado(), error="Error en el proceso de buscar producto", formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())




# Cambia de estado bloqueo STIVEN
@app.route('/productos/gestion/edit/BlockProducto=<referencia><estado>')
def block_producto(referencia, estado):
    obj_proEstado =producto.block(referencia, estado)
    if obj_proEstado:
        if estado == "T":
            obj_proEstado="Producto con "+ referencia+" bloqueado "
        elif estado == "F":
            obj_proEstado="Producto con "+ referencia+" desbloqueado "
        return render_template('gestion_productos.html',mensaje=obj_proEstado,lista_productos=producto.listado(), block=estado,formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
    return render_template('gestion_productos.html',error="No se pudo bloquear al producto",lista_productos=producto.listado(),formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())

# Medtodo de actualizar datos STIVEN
@app.route('/productos/gestion/<id>', methods=["GET", "POST"])
def editar_producto(id):
    if request.method == "GET":
        formulario = FormGestionProducto()
        obj_mensaje =producto.cargar(id)
        if obj_mensaje:
            formulario.nombre.data = obj_mensaje.nombre
            formulario.referencia.data = obj_mensaje.referencia
            formulario.talla.data = obj_mensaje.talla
            formulario.precio.data = obj_mensaje.precio
            formulario.cantidad.data = obj_mensaje.cantidad
            formulario.descuento.data = obj_mensaje.descuento
            formulario.color.data = obj_mensaje.color
            formulario.descripcion.data = obj_mensaje.descripcion
            formulario.sexo.data = obj_mensaje.sexo
            return render_template('gestion_productos.html',producto=obj_mensaje,lista_productos=producto.listado(), opcion="Editar", form=formulario,formBuscar=FormBuscar(),lista_productosSer=producto.listado_searchs())
        return render_template('gestion_productos.html',error="No existe el producto",lista_productos=producto.listado(),formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
    else:
        formulario = FormGestionProducto(request.form)
        if formulario.validate_on_submit():
            obj_usuario = producto.editar(id,formulario.nombre.data,formulario.referencia.data,formulario.talla.data,formulario.precio.data,formulario.cantidad.data,formulario.descuento.data,formulario.color.data,formulario.descripcion.data,formulario.sexo.data)
            if obj_usuario:
                obj_usuario =producto.cargar(id)
                return render_template('gestion_productos.html',producto=obj_usuario,lista_productos=producto.listado(), opcion="Editar",form=FormGestionProducto(), mensaje="Editado correctamente",formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
        return render_template('gestion_productos.html',lista_productos=producto.listado(), error="Verifique los datos ingresados",form=FormGestionProducto(),formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())

# Crear productos, plantilla gestion STIVEN
@app.route('/productos/gestion/crear', methods=["GET", "POST"])
def crear_producto():
    if request.method == "GET":
        formulario = FormGestionProducto()
        return render_template('gestion_productos.html',lista_productos=producto.listado(), opcion="Crear", form=formulario, lista_productosSer=producto.listado_searchs())
    else:
        formulario = FormGestionProducto(request.form)
        if formulario.validate_on_submit():
            obj_crearProducto = producto('',formulario.nombre.data, formulario.referencia.data, formulario.talla.data, formulario.precio.data,formulario.cantidad.data,formulario.descuento.data,formulario.color.data, formulario.descripcion.data, formulario.sexo.data, lista_productos=producto.listado_searchs())
            if (obj_crearProducto.crear()):
                return render_template('gestion_productos.html',producto=obj_crearProducto,lista_productos=producto.listado(), opcion="Editar",form=FormGestionProducto(), mensaje="Creado correctamente el producto "+ formulario.nombre.data,formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())

            return render_template('gestion_productos.html',lista_productos=producto.listado(), error="Error en el proceso de crear producto",opcion="Crear",form=FormGestionProducto(),formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
        return render_template('gestion_productos.html',lista_productos=producto.listado(), error="Error en el proceso de crear producto",opcion="Crear",form=FormGestionProducto(),formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())

@app.route('/productos/gestion/Delete/<id>')
def delete_producto(id):
    obj_usuario =producto.delete(id)
    if obj_usuario:
        obj_usuario+= id
        return render_template('gestion_productos.html',mensaje=obj_usuario,lista_productos=producto.listado(),formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
    return render_template('gestion_productos.html',error="No se pudo eliminar al producto "+id,lista_productos=producto.listado(),formBuscar=FormBuscar(), lista_productosSer=producto.listado_searchs())
# ------------------------------------------------------------------------------------------------------

"""-----------------INICIO GESTIÓN DE PERFIL (MI CUENTA)------------------"""
@app.route('/gestion/micuenta/<documento>', methods = ["GET", "POST"])
def gestion_micuenta(documento):
    if request.method == "GET":
        formulario = FormMiCuenta()
        obj_usuario = gestionMiCuenta.cargar_datos(documento)
        if obj_usuario:
            formulario.nombre.data = obj_usuario.nombre
            formulario.apellidos.data = obj_usuario.apellido
            formulario.documento.data = obj_usuario.documento
            formulario.sexo.data = obj_usuario.sexo
            formulario.nickname.data = obj_usuario.nickname
            formulario.telefono.data = obj_usuario.telefono
            formulario.correo.data = obj_usuario.correo
            formulario.pais.data = obj_usuario.pais
            formulario.departamento.data = obj_usuario.departamento
            formulario.ciudad.data = obj_usuario.ciudad
            formulario.direccion.data = obj_usuario.direccion
            formulario.contrasena.data = ""
            formulario.contrasenaNueva.data = ""
            formulario.confirmarContrasenaNueva.data = ""
            return render_template('gestion_micuenta.html', datosUsuario = obj_usuario, form = formulario, documento=documento, lista_productosSer=producto.listado_searchs())
        return render_template('gestion_micuenta.html', error= "No existe el usuario" , form = formulario, lista_productosSer=producto.listado_searchs())
    else:
        formulario = FormMiCuenta (request.form)
        if formulario.validate_on_submit:
            obj_usuario = gestionMiCuenta.cargar_datos(documento)
            
            if obj_usuario:

                obj_logear= usuario(formulario.nickname.data, formulario.documento.data, formulario.correo.data, formulario.contrasena.data,'')
                if obj_logear.logear():

                    obj_usuario.nombre = formulario.nombre.data
                    obj_usuario.apellido = formulario.apellidos.data
                    obj_usuario.documento = formulario.documento.data
                    obj_usuario.sexo = formulario.sexo.data
                    obj_usuario.nickname = formulario.nickname.data
                    obj_usuario.telefono = formulario.telefono.data
                    obj_usuario.correo = formulario.correo.data
                    obj_usuario.pais = formulario.pais.data
                    obj_usuario.departamento = formulario.departamento.data
                    obj_usuario.ciudad = formulario.ciudad.data
                    obj_usuario.direccion = formulario.direccion.data
                    if len(formulario.contrasenaNueva.data)>0:
                        obj_usuario.contrasena = formulario.contrasenaNueva.data
                    else:
                        obj_usuario.contrasena = formulario.contrasena.data
                    obj_usuario.editar_datos()
                    return render_template ('gestion_micuenta.html', datosUsuario = obj_usuario, form = formulario, mensaje = "Se han editado correctamente los datos", lista_productosSer=producto.listado_searchs())

            return render_template ('gestion_micuenta.html', datosUsuario = obj_usuario, form = formulario, error = "Error en el proceso de edición de los datos")

    return render_template('gestion_micuenta.html', form=FormMiCuenta(), lista_productosSer=producto.listado_searchs())

"""-----------------INICIO GESTIÓN SUPERADMINISTRADOR------------------"""
@app.route('/superadministrador/')
def superadministrador():
    return render_template('superadministrador.html', formBuscar=FormBuscarAdministrador(), listaAdmin=gestionAdministrador.listado_administrador(), lista_productosSer=producto.listado_searchs())

@app.route('/superadministrador/gestionar/<documento>',  methods = ["GET", "POST"])
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
            formulario.contrasena.data = ""
            formulario.confirmarcontrasena.data = ""
            return render_template('superadministrador.html', datosAdministrador = obj_admin, form = formulario, formBuscar = FormBuscarAdministrador(), listaAdmin = gestionAdministrador.listado_administrador(), opcion = "Editar", lista_productosSer=producto.listado_searchs())
        return render_template('superadministrador.html', error = "No existe el usuario", formBuscar = FormBuscarAdministrador(), listaAdmin = gestionAdministrador.listado_administrador(), lista_productosSer=producto.listado_searchs())
    else:
        formulario = FormGestionar(request.form)
        if formulario.validate_on_submit():
            obj_admin = gestionAdministrador.cargar_datos(documento)
            if obj_admin:
                obj_admin.nombre = formulario.nombre.data
                obj_admin.apellido = formulario.apellidos.data
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
                return render_template('superadministrador.html', datosAdministrador = obj_admin, formBuscar = FormBuscarAdministrador(), listaAdmin = gestionAdministrador.listado_administrador(), mensaje = "Se han editado los datos del administrador {0} {1} correctamente".format(formulario.nombre.data, formulario.apellidos.data), opcion = "Editar", lista_productosSer=producto.listado_searchs())
        return render_template('superadministrador.html', form = FormGestionar(), formBuscar = FormBuscarAdministrador(), listaAdmin = gestionAdministrador.listado_administrador(), error = "Verifique los datos ingresados", lista_productosSer=producto.listado_searchs())

@app.route('/superadministrador/crear/', methods = ["GET", "POST"])
def crear_administrador():
    if request.method == "GET":
        formulario = FormGestionar()
        return render_template('superadministrador.html', form = formulario, listaAdmin = gestionAdministrador.listado_administrador(), formBuscar = FormBuscarAdministrador(), opcion="Crear", lista_productosSer=producto.listado_searchs())
    else:
        formulario = FormGestionar(request.form)
        if formulario.validate_on_submit():
            obj_admin = gestionAdministrador(formulario.nombre.data, formulario.apellidos.data, formulario.documento.data, formulario.sexo.data, formulario.nickname.data, formulario.telefono.data, formulario.correo.data, formulario.pais.data, formulario.departamento.data, formulario.ciudad.data, formulario.direccion.data, formulario.contrasena.data, "admin", "T")
            if (obj_admin.crear_admin()):
                return render_template('superadministrador.html', mensaje = "Se ha creado correctamente el administrador {0} {1} correctamente".format(formulario.nombre.data, formulario.apellidos.data), listaAdmin = gestionAdministrador.listado_administrador(), formBuscar = FormBuscarAdministrador(), opcion="Editar", datosAdministrador = obj_admin, form = FormGestionar(), lista_productosSer=producto.listado_searchs())
        return render_template('superadministrador.html', error = "Error en el proceso de creación del administrador",form = FormGestionar(), listaAdmin = gestionAdministrador.listado_administrador(), formBuscar = FormBuscarAdministrador(), opcion = "Crear", lista_productosSer=producto.listado_searchs())

@app.route('/superadministrador/eliminar/<documento>')
def eliminar_administrador(documento):
    obj_admin = gestionAdministrador.cargar_datos(documento)
    if obj_admin.eliminar_admin():
        return render_template('superadministrador.html', mensaje = "Se ha eliminado correctamente el administrador {0}".format(documento), listaAdmin = gestionAdministrador.listado_administrador(), formBuscar = FormBuscarAdministrador(), lista_productosSer=producto.listado_searchs())
    return render_template('superadministrador.html', error = "Error en la eliminación del administrador", listaAdmin = gestionAdministrador.listado_administrador(), formBuscar = FormBuscarAdministrador(), lista_productosSer=producto.listado_searchs())
    
@app.route('/superadministrador/bloquear/<documento>')
def bloquear_administrador(documento):
    obj_admin = gestionAdministrador.cargar_datos(documento)
    obj_admin.bloquear_admin()
    if obj_admin.estado == "F":
        return render_template('superadministrador.html', mensaje = "Se ha desbloqueado el administrador {0}".format(documento), listaAdmin = gestionAdministrador.listado_administrador(),formBuscar=FormBuscarAdministrador(), lista_productosSer=producto.listado_searchs())
    elif obj_admin.estado == "T":
        return render_template('superadministrador.html', mensaje = "Se ha bloqueado el administrador {0}".format(documento), listaAdmin = gestionAdministrador.listado_administrador(),formBuscar = FormBuscarAdministrador(), lista_productosSer=producto.listado_searchs())
    return render_template('superadministrador.html', mensaje = "No se ha podido cambiar el estado del administrador {0}".format(documento), listaAdmin=gestionAdministrador.listado_administrador(),formBuscar=FormBuscarAdministrador(), lista_productosSer=producto.listado_searchs())

@app.route('/superadministrador/buscar/', methods=["GET", "POST"])
def Buscar_administrador():
    if request.method == "GET":
        return render_template('superadministrador.html',listaAdmin = gestionAdministrador.listado_administrador(),formBuscar = FormBuscarAdministrador(), form = FormGestionar(), lista_productosSer=producto.listado_searchs())
    else:
        formBuscar = FormBuscarAdministrador(request.form)
        formulario = FormGestionar()
        if formBuscar.validate_on_submit():
            obj_admin = gestionAdministrador.cargar_datos(formBuscar.buscar.data)
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
                formulario.contrasena.data = ""
                return render_template('superadministrador.html', datosAdministrador=obj_admin, form=formulario, formBuscar=FormBuscarAdministrador(), listaAdmin=gestionAdministrador.listado_administrador(), opcion="Editar", lista_productos=producto.listado_searchs(), lista_productosSer=producto.listado_searchs())
            return render_template('superadministrador.html', form=formulario, formBuscar=FormBuscarAdministrador(), listaAdmin=gestionAdministrador.listado_administrador(), opcion="Crear", error = "No exite el administrador {o}, puede crearlo".format(formBuscar.buscar.data), lista_productosSer=producto.listado_searchs())
        return render_template('superadministrador.html', form=formulario, formBuscar=FormBuscarAdministrador(), listaAdmin=gestionAdministrador.listado_administrador(), opcion="Crear", error = "Error en el proceso de busqueda", lista_productosSer=producto.listado_searchs())



"""Ruta para todos los comentarios de un producto"""
@app.route('/comentarios/')
def todos_los_comentarios():
    return render_template('todos_los_comentarios.html', lista_productosSer=producto.listado_searchs())

@app.route('/contactos/')
def contactos():
    return render_template('contactos.html', lista_productosSer=producto.listado_searchs())


#---------------Direccion de linkedi----------------------

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