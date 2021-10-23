from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField, SubmitField, TextAreaField
from wtforms import validators

class FormGestionar(FlaskForm):
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
    precio=StringField('Precio', validators=[validators.required(),validators.length(max=10)])
    cantidad = StringField('Stock', validators=[validators.required(),validators.length(max=1)])
    descuento = StringField('Descuento Comercial', validators=[validators.required(),validators.length(max=20)])
    color = StringField('Color', validators=[validators.required(),validators.length(max=20)])
    descripcion = StringField('Descripción', validators=[validators.required(),validators.length(max=150)])
    sexo = StringField('Sexo', validators=[validators.required(),validators.length(max=1)])
    agregar = SubmitField('Agregar')


class FormGestionarComentario(FlaskForm):
    comentario = TextAreaField('opinión',[validators.length(max=300)])

class FormBuscarAdministrador(FlaskForm):
    buscar = StringField('Buscar')

