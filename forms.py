from os import read, readlink
from models import *
from flask_wtf import FlaskForm
from wtforms.fields.core import SelectField, StringField
from wtforms.fields.simple import PasswordField, SubmitField, TextAreaField
from wtforms import validators


class FormGestionar(FlaskForm):
    nombre = StringField('Nombre',validators=[validators.required()])
    apellidos = StringField('Apellidos', validators=[validators.required()])
    documento = StringField('Documento')
    sexo = StringField('Sexo', validators=[validators.required()])
    correo = StringField('Correo', validators=[validators.required()])
    nickname = StringField('Nickname', validators=[validators.required()])
    telefono = StringField('Celular', validators=[validators.required()])
    contrasena = StringField('Contraseña', validators=[validators.required(),validators.length(max=150)])
    confirmarcontrasena = StringField('Confirmar contraseña', validators=[validators.required(),validators.length(max=150)])
    pais = StringField('País', validators=[validators.required(),validators.length(max=50)])
    departamento = StringField('Departamento', validators=[validators.required(),validators.length(max=50)])
    ciudad = StringField('Ciudad', validators=[validators.required(),validators.length(max=50)])
    direccion = StringField('Dirección', validators=[validators.required(),validators.length(max=200)])
    agregar = SubmitField('Agregar')
    registro = SubmitField('Registro')
    guardarCambios = SubmitField('Guardar cambios')
    editar = SubmitField('Editar')
    crear = SubmitField ('Crear')
    login = SubmitField('Iniciar sesión')
    

class FormBuscar(FlaskForm):
    buscar = StringField('buscar')

class FormGestionProducto(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[validators.required(),validators.length(max=150)])
    referencia = StringField('Referencia', validators=[validators.required(),validators.length(max=150)])
    talla = StringField('Talla', validators=[validators.required(),validators.length(max=150)])
    precio=StringField('Precio', validators=[validators.required()])
    cantidad = StringField('Stock', validators=[validators.required(),validators.length(max=100)])
    descuento = StringField('Descuento Comercial', validators=[validators.required(),validators.length(max=20)])
    color = StringField('Color', validators=[validators.required(),validators.length(max=20)])
    descripcion = StringField('Descripción', validators=[validators.required(),validators.length(max=1000)])
    sexo = StringField('Sexo', validators=[validators.required(),validators.length(max=1)])
    agregar = SubmitField('Agregar')

class FormGestionarComentario(FlaskForm):
    comentario = TextAreaField('opinión',[validators.length(max=300)])

class FormBuscarAdministrador(FlaskForm):
    buscar = StringField('Buscar')

class FormFiltrarProductoIndividual(FlaskForm):
    talla = SelectField(u'talla', choices=[
        ('0','Seleccionar talla'),
        ##(lista.talla,lista.talla) for lista in producto.productoindividual("ML515SM3")
        ])
class FormFiltrarProducto(FlaskForm):
    orden = SelectField(u'orden', choices=[('0','Seleccionar orden'),('asc','Menor precio'), ( 'desc','Mayor precio')])

    talla = SelectField(u'talla', choices=[('0','Seleccionar talla'),('35', '35'), ('35.5', '35.5'),('36', '36'),('36.5', '36.5'),('37', '37'),('37.5', '37.5'),('38', '38'),('38.5', '38.5'),('39', '39'),('39.5', '39.5'),('40', '40'),('40.5', '40.5'),('41', '41'),('41.5', '41.5')])
    
    color = SelectField(u'color', choices=[('0', 'Seleccionar color'),('negro', 'Negro'), ('naranja', 'Naranja'),('amarillo', 'Amarillo'),('azul', 'Azul'),('rojo', 'Rojo'),('café', 'Café'),('gris', 'Gris'),('rosa', 'Rosa'),('verde', 'Verde'),('blanco', 'Blanco'),('multicolor', 'Multicolor')])
    
    # unidad = SelectField(u'unidad', choices=[('0','Seleccionar unidad'),('1','1'), ( '2','2'), ( '3','3'), ( '4','4')])

class FormMiCuenta(FlaskForm):
    nombre = StringField('Nombre',validators=[validators.required()])
    apellidos = StringField('Apellidos', validators=[validators.required()])
    documento = StringField('Documento', validators=[validators.required()])
    sexo = StringField('Sexo', validators=[validators.required()])
    correo = StringField('Correo', validators=[validators.required()])
    nickname = StringField('Nickname', validators=[validators.required()])
    telefono = StringField('Celular', validators=[validators.required()])
    contrasena = StringField('Contraseña', validators=[validators.required(),validators.length(max=150)])
    confirmarcontrasena = StringField('Confirmar contraseña', validators=[validators.required(),validators.length(max=150)])
    pais = StringField('País', validators=[validators.required(),validators.length(max=50)])
    departamento = StringField('Departamento', validators=[validators.required(),validators.length(max=50)])
    ciudad = StringField('Ciudad', validators=[validators.required(),validators.length(max=50)])
    direccion = StringField('Dirección', validators=[validators.required(),validators.length(max=200)])
    contrasenaNueva = StringField('Nueva contraseña', validators=[validators.length(max=150)])
    confirmarContrasenaNueva = StringField('Confirmar contraseña"', validators=[validators.length(max=150)])
    guardarCambios = SubmitField('Guardar cambios')
