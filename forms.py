from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField, TextAreaField
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