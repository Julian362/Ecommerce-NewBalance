from flask_wtf import FlaskForm
from wtforms.fields.core import RadioField, StringField
from wtforms.fields.simple import PasswordField, SubmitField, TextAreaField
from wtforms import validators
from wtforms.widgets.core import CheckboxInput, Input, SubmitInput, TextArea

class FormEditUsuario(FlaskForm):
    nombre = StringField('Nombre',validators=[validators.required()])
    apellidos = StringField('Apellidos')
    documento = StringField('Documento', validators=[validators.required()])
    sexo = StringField('Sexo', validators=[validators.required()])
    correo = StringField('Correo', validators=[validators.required()])
    nickname = StringField('Nickname', validators=[validators.required()])
    celular = StringField('Celular', validators=[validators.required()])
    contrasena = PasswordField('Contraseña', validators=[validators.required(),validators.length(max=150)])
    confirmarcontrasena = PasswordField('Confirmar contraseña', validators=[validators.required(),validators.length(max=150)])
    pais = StringField('País', validators=[validators.required(),validators.length(max=50)])
    departamento = StringField('Departamento', validators=[validators.required(),validators.length(max=50)])
    ciudad = StringField('Ciudad', validators=[validators.required(),validators.length(max=50)])
    direccion = StringField('Dirección', validators=[validators.required(),validators.length(max=200)])

class FormCrearUsuario(FlaskForm):
    nombre = StringField('Nombre',validators=[validators.required()])
    apellidos = StringField('Apellidos')
    documento = StringField('Documento', validators=[validators.required()])
    sexo = StringField('Sexo', validators=[validators.required()])
    correo = StringField('Correo', validators=[validators.required()])
    nickname = StringField('Nickname', validators=[validators.required()])
    celular = StringField('Celular', validators=[validators.required()])
    contrasena = PasswordField('Contraseña', validators=[validators.required(),validators.length(max=150)])
    confirmarcontrasena = PasswordField('Confirmar contraseña', validators=[validators.required(),validators.length(max=150)])
    pais = StringField('País', validators=[validators.required(),validators.length(max=50)])
    departamento = StringField('Departamento', validators=[validators.required(),validators.length(max=50)])
    ciudad = StringField('Ciudad', validators=[validators.required(),validators.length(max=50)])
    direccion = StringField('Dirección', validators=[validators.required(),validators.length(max=200)])
    agregar = SubmitField('Agregar')

class FormBuscar(FlaskForm):
    buscar = StringField('buscar')

class FormRegistro(FlaskForm):
    nombre = StringField('Nombre', validators=[validators.required(),validators.length(max=150)])
    apellido = StringField('Apellidos', validators=[validators.required(),validators.length(max=150)])
    correo = StringField('Correo', validators=[validators.required(),validators.length(max=150)])
    nickname=StringField('Nickname', validators=[validators.required(),validators.length(max=10)])
    sexo = StringField('Sexo', validators=[validators.required(),validators.length(max=1)])
    documento = StringField('Documento', validators=[validators.required(),validators.length(max=20)])
    telefono = StringField('Teléfono Celular', validators=[validators.required(),validators.length(max=20)])
    contrasena = PasswordField('Contraseña', validators=[validators.required(),validators.length(max=150)])
    confirmarContraseña = PasswordField('Confirmar Contraseña', validators=[validators.required(),validators.length(max=150)])
    pais = StringField('País', validators=[validators.required(),validators.length(max=50)])
    departamento = StringField('Departamento', validators=[validators.required(),validators.length(max=50)])
    ciudad = StringField('Ciudad', validators=[validators.required(),validators.length(max=50)])
    direccion = StringField('Dirección', validators=[validators.required(),validators.length(max=200)])
    registro = SubmitField('Registro')

class FormGestionProducto(FlaskForm):
    nombre = StringField('Nombre del Producto', validators=[validators.required(),validators.length(max=150)])
    referencia = StringField('Referencia', validators=[validators.required(),validators.length(max=150)])
    talla = StringField('Talla', validators=[validators.required(),validators.length(max=150)])
    precio=StringField('Precio', validators=[validators.required(),validators.length(max=10)])
    cantidad = StringField('Stock', validators=[validators.required(),validators.length(max=1)])
    descuento = StringField('Descuento Comercial', validators=[validators.required(),validators.length(max=20)])
    color = StringField('Color', validators=[validators.required(),validators.length(max=20)])
    descripcion = PasswordField('Descripción', validators=[validators.required(),validators.length(max=150)])
    sexo = StringField('Sexo', validators=[validators.required(),validators.length(max=1)])
    agregar = SubmitField('Agregar')

class FormGestionarComentario(FlaskForm):
    opinion = TextAreaField('opinión',[validators.length(max=300)])

class FormMiCuenta(FlaskForm):
    nombre = StringField('Nombre', validators=[validators.required(),validators.length(max=150)])
    apellido = StringField('Apellidos', validators=[validators.required(),validators.length(max=150)])
    documento = StringField('Documento', validators=[validators.required(),validators.length(max=20)])
    nickname = StringField('Nickname', validators=[validators.required(),validators.length(max=20)])
    telefono = StringField('Teléfono Celular', validators=[validators.required(),validators.length(max=20)])
    correo = StringField('Correo', validators=[validators.required(),validators.length(max=150)])
    sexo = StringField('Sexo', validators=[validators.required(),validators.length(max=1)])
    pais = StringField('País', validators=[validators.required(),validators.length(max=50)])
    departamento = StringField('Departamento', validators=[validators.required(),validators.length(max=50)])
    ciudad = StringField('Ciudad', validators=[validators.required(),validators.length(max=50)])
    direccion = StringField('Dirección', validators=[validators.required(),validators.length(max=200)])
    contrasena = PasswordField('Contraseña', validators=[validators.required(),validators.length(max=150)])
    contrasenaNueva = PasswordField('Confirmar Contraseña', validators=[validators.required(),validators.length(max=150)])
    confirmarContrasenaNueva = PasswordField('Confirmar Contraseña', validators=[validators.required(),validators.length(max=150)])
    guardarCambios = SubmitField('Guardar cambios')

class FormBuscarAdministrador(FlaskForm):
    buscar = StringField('Buscar')
class FormAdministrador(FlaskForm):
    nombre = StringField('Nombre', validators=[validators.required(),validators.length(max=150)])
    apellido = StringField('Apellidos', validators=[validators.required(),validators.length(max=150)])
    documento = StringField('Documento', validators=[validators.required(),validators.length(max=20)])
    nickname = StringField('Nickname', validators=[validators.required(),validators.length(max=20)])
    telefono = StringField('Teléfono Celular', validators=[validators.required(),validators.length(max=20)])
    correo = StringField('Correo', validators=[validators.required(),validators.length(max=150)])
    sexo = StringField('Sexo', validators=[validators.required(),validators.length(max=1)])
    pais = StringField('País', validators=[validators.required(),validators.length(max=50)])
    departamento = StringField('Departamento', validators=[validators.required(),validators.length(max=50)])
    ciudad = StringField('Ciudad', validators=[validators.required(),validators.length(max=50)])
    direccion = StringField('Dirección', validators=[validators.required(),validators.length(max=200)])
    contrasena = PasswordField('Contraseña', validators=[validators.required(),validators.length(max=150)])
    confirmarCcontrasena = PasswordField('Contraseña', validators=[validators.required(),validators.length(max=150)])
    editar = SubmitField('Editar')
    
class FormLogin(FlaskForm):
    correo = StringField('Correo', validators=[validators.required()])
    contrasena = PasswordField('Contraseña', validators=[validators.required()])
    login = SubmitField('Iniciar sesión')

