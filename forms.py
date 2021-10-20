from flask_wtf import FlaskForm
from wtforms.fields.core import RadioField, StringField
from wtforms.fields.simple import PasswordField, SubmitField, TextAreaField
from wtforms import validators
from wtforms.widgets.core import CheckboxInput, Input, SubmitInput, TextArea

class FormEditUsuario(FlaskForm):
    nombre = StringField('Nombre',validators=[validators.required()])
    apellidos = StringField('Apellidos')
    correo = StringField('Correo', validators=[validators.required()])
    documento = StringField('Documento', validators=[validators.required()])
    celular = StringField('Celular', validators=[validators.required()])
    sexo = StringField('Sexo', validators=[validators.required()])

class FormCrearUsuario(FlaskForm):
    nombre = StringField('Nombre',validators=[validators.required()])
    apellidos = StringField('Apellidos')
    correo = StringField('Correo', validators=[validators.required()])
    documento = StringField('Documento', validators=[validators.required()])
    nickname = StringField('Nickname', validators=[validators.required()])
    celular = StringField('Celular', validators=[validators.required()])
    sexo = StringField('Sexo', validators=[validators.required()])

class FormBuscar(FlaskForm):
    buscar = StringField('buscar')

class FormRegistro(FlaskForm):
    nombre = StringField('Nombre', validators=[validators.required(),validators.length(max=150)])
    apellido = StringField('Apellidos', validators=[validators.required(),validators.length(max=150)])
    correo = StringField('Correo', validators=[validators.required(),validators.length(max=150)])
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

class FormGestionarComentario(FlaskForm):
    opinion = StringField('opinión',validators.length(max=300))