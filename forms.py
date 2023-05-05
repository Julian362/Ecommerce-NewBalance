from os import read, readlink
from models import *
from flask_wtf import FlaskForm
from wtforms.fields.core import SelectField, StringField
from wtforms.fields.simple import PasswordField, SubmitField, TextAreaField
from wtforms import validators


class FormManage(FlaskForm):
    name = StringField("Nombre", validators=[validators.required()])
    last_name = StringField("Apellidos", validators=[validators.required()])
    document = StringField("Documento")
    gender = StringField("Genero", validators=[validators.required()])
    email = StringField("Correo", validators=[validators.required()])
    nickname = StringField("Nickname", validators=[validators.required()])
    phone = StringField("Celular", validators=[validators.required()])
    password = StringField(
        "Contraseña", validators=[validators.required(), validators.length(max=150)]
    )
    confirm_password = StringField(
        "Confirmar contraseña",
        validators=[validators.required(), validators.length(max=150)],
    )
    country = StringField(
        "País", validators=[validators.required(), validators.length(max=50)]
    )
    department = StringField(
        "Departamento", validators=[validators.required(), validators.length(max=50)]
    )
    city = StringField(
        "Ciudad", validators=[validators.required(), validators.length(max=50)]
    )
    address = StringField(
        "Dirección", validators=[validators.required(), validators.length(max=200)]
    )
    add = SubmitField("Agregar")
    register = SubmitField("Registro")
    save = SubmitField("Guardar cambios")
    edit = SubmitField("Editar")
    create = SubmitField("Crear")
    login = SubmitField("Iniciar sesión")


class FormSearch(FlaskForm):
    search = StringField("buscar")


class FormManagementProduct(FlaskForm):
    name = StringField(
        "Nombre del Producto",
        validators=[validators.required(), validators.length(max=150)],
    )
    reference = StringField(
        "Referencia", validators=[validators.required(), validators.length(max=150)]
    )
    size = StringField(
        "Talla", validators=[validators.required(), validators.length(max=150)]
    )
    price = StringField("Precio", validators=[validators.required()])
    amount = StringField(
        "Stock", validators=[validators.required(), validators.length(max=100)]
    )
    discount = StringField(
        "Descuento Comercial",
        validators=[validators.required(), validators.length(max=20)],
    )
    color = StringField(
        "Color", validators=[validators.required(), validators.length(max=20)]
    )
    description = StringField(
        "Descripción", validators=[validators.required(), validators.length(max=1000)]
    )
    gender = StringField(
        "Genero", validators=[validators.required(), validators.length(max=1)]
    )
    add = SubmitField("Agregar")


class FormManageComment(FlaskForm):
    comment = TextAreaField("opinión", [validators.length(max=300)])


class FormSearchAdmin(FlaskForm):
    search = StringField("Buscar")


class FormFilterProductIndividual(FlaskForm):
    size = SelectField(
        "talla",
        choices=[
            ("0", "Seleccionar talla"),
            ##(lista.talla,lista.talla) for lista in producto.productoindividual("ML515SM3")
        ],
    )


class FormFilterProduct(FlaskForm):
    orden = SelectField(
        "orden",
        choices=[
            ("0", "Seleccionar orden"),
            ("asc", "Menor precio"),
            ("desc", "Mayor precio"),
        ],
    )

    size = SelectField(
        "talla",
        choices=[
            ("0", "Seleccionar talla"),
            ("35", "35"),
            ("35.5", "35.5"),
            ("36", "36"),
            ("36.5", "36.5"),
            ("37", "37"),
            ("37.5", "37.5"),
            ("38", "38"),
            ("38.5", "38.5"),
            ("39", "39"),
            ("39.5", "39.5"),
            ("40", "40"),
            ("40.5", "40.5"),
            ("41", "41"),
            ("41.5", "41.5"),
        ],
    )

    color = SelectField(
        "color",
        choices=[
            ("0", "Seleccionar color"),
            ("negro", "Negro"),
            ("naranja", "Naranja"),
            ("amarillo", "Amarillo"),
            ("azul", "Azul"),
            ("rojo", "Rojo"),
            ("café", "Café"),
            ("gris", "Gris"),
            ("rosa", "Rosa"),
            ("verde", "Verde"),
            ("blanco", "Blanco"),
            ("multicolor", "Multicolor"),
        ],
    )


class FormMyAccount(FlaskForm):
    name = StringField("Nombre", validators=[validators.required()])
    last_name = StringField("Apellidos", validators=[validators.required()])
    document = StringField("Documento", validators=[validators.required()])
    gender = StringField("Genero", validators=[validators.required()])
    email = StringField("Correo", validators=[validators.required()])
    nickname = StringField("Nickname", validators=[validators.required()])
    phone = StringField("Celular", validators=[validators.required()])
    password = StringField(
        "Contraseña", validators=[validators.required(), validators.length(max=150)]
    )
    confirm_password = StringField(
        "Confirmar contraseña",
        validators=[validators.required(), validators.length(max=150)],
    )
    country = StringField(
        "País", validators=[validators.required(), validators.length(max=50)]
    )
    department = StringField(
        "Departamento", validators=[validators.required(), validators.length(max=50)]
    )
    city = StringField(
        "Ciudad", validators=[validators.required(), validators.length(max=50)]
    )
    address = StringField(
        "Dirección", validators=[validators.required(), validators.length(max=200)]
    )
    new_password = StringField(
        "Nueva contraseña", validators=[validators.length(max=150)]
    )
    confirm_new_password = StringField(
        'Confirmar contraseña"', validators=[validators.length(max=150)]
    )
    save = SubmitField("Guardar cambios")
