import os
import functools
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    request,
    g,
    url_for,
    session,
)
from flask.wrappers import Request
from models import *
from forms import *
from werkzeug.utils import redirect

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def index():
    return render_template("index.html", list_product_ser=Product.list_search())


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login"))
        return view(**kwargs)

    return wrapped_view


@app.before_request
def load_user():
    user_email = session.get("user_email")
    if user_email is None:
        g.user = None
    else:
        g.user = User.load(user_email)


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "GET":
        return render_template(
            "login.html",
            form=FormManage(),
            list_product_ser=Product.list_search(),
        )
    else:
        formulario = FormManage(request.form)
        obj_user = User("", "", formulario.email.data, formulario.password.data, "")
        if (
            not obj_user.email.__contains__("'")
            and not obj_user.password.__contains__("'")
            and obj_user.logging()
        ):
            session.clear()
            session["user_email"] = obj_user.email
            return redirect("/")
        return render_template(
            "login.html",
            error="Usuario o contraseña invalido",
            form=FormManage(),
            list_product_ser=Product.list_search(),
        )


@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/registro/", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template(
            "register.html",
            form=FormManage(),
            list_product_ser=Product.list_search(),
        )
    else:
        frm_register = FormManage(request.form)
        if frm_register.validate_on_submit:
            obj_register = Person(
                frm_register.document.data,
                frm_register.nickname.data,
                frm_register.name.data,
                frm_register.last_name.data,
                frm_register.email.data,
                frm_register.phone.data,
                frm_register.gender.data,
                frm_register.address.data,
                frm_register.country.data,
                frm_register.department.data,
                frm_register.city.data,
                frm_register.password.data,
                "user",
                "T",
            )
            if obj_register.insertar_registro():
                return redirect(url_for("login"))
            return render_template(
                "register.html",
                form=FormManage(),
                error="Algo falló al intentar registrar sus datos, intente nuevamente",
                list_product_ser=Product.list_search(),
            )
        return render_template(
            "register.html",
            form=FormManage(),
            error="Todos los campos son requeridos, verifique los campos e intente nuevamente",
            list_product_ser=Product.list_search(),
        )


@app.route("/product/<reference>")
def product(reference):
    average = 0
    accumulator = 0
    list_calification = Calification.all_comments(reference)
    for i in list_calification:
        accumulator += i["rating"]
    if len(list_calification) > 0:
        average = accumulator / len(list_calification)
    return render_template(
        "product.html",
        Product_reference=Product.list_search_product(reference),
        item=Product.load(reference),
        form=FormFilterProductIndividual(),
        list_comments=Calification.all_comments(reference),
        average=average,
        average_comments=Calification.average_comments(reference),
        tres_registros=Calification.limit_comments(reference),
        filter=FormFilterProduct(),
    )


@app.route("/cart/<document>")
def cart(document):
    list_cart = Product.load_cart(document)
    total = 0
    for i in list_cart:
        total += i["price"]
    return render_template(
        "cart.html",
        list_cart=list_cart,
        total=total,
        filter=FormFilterProduct(),
    )


@app.route("/<document>-<reference>", methods=["POST"])
def add_cart(document, reference):
    if request.method == "POST":
        form = FormFilterProduct(request.form)
        if Product.create_cart(reference, document, form.size.data, form.color.data):
            return redirect(url_for("product", reference=reference))
        return redirect(url_for("product", reference=reference))


@app.route("/<id>--<document>", methods=["POST"])
def delete_product_cart(id, document):
    if request.method == "POST":
        Product.delete_cart(id)
        return redirect(url_for("cart", document=document))


@app.route(
    "/comentario/gestionar/crear/<reference>-<rating>-<document>",
    methods=["GET", "POST"],
)
def create_comment(reference, rating, document):
    if request.method == "GET":
        form = FormManageComment()
        obj_calification = Calification(
            "", 0, "", reference, Person.load("user", document).nickname, document
        )
        return render_template(
            "comments.html",
            option="Crear",
            form=form,
            calificationCreate=obj_calification,
            list_product_ser=Product.list_search(),
        )
    else:
        form = FormManageComment(request.form)
        obj_calification = Calification(
            "",
            rating,
            form.comment.data,
            reference,
            Person.load("user", document).nickname,
            document,
        )
        if form.validate_on_submit():
            if obj_calification.create():
                return redirect(url_for("product", reference=reference))
            return render_template(
                "comments.html",
                option="Crear",
                form=form,
                calificationCreate=obj_calification,
                error="No se pudo crear el comentario ",
            )
        return render_template(
            "comments.html",
            option="Crear",
            form=form,
            calificationCreate=obj_calification,
            error="No se pudo validar el crear el comentario ",
        )


@app.route(
    "/comentario/gestionar/editar/<reference>-<rating>-<document>",
    methods=["GET", "POST"],
)
def edit_comment(reference, rating, document):
    if request.method == "GET":
        obj_calification = Calification.load(document, reference)
        form = FormManageComment()
        form.comment.data = obj_calification.comentario
        return render_template(
            "comments.html",
            option="Editar",
            form=form,
            calification=obj_calification,
            list_product_ser=Product.list_search(),
        )
    else:
        form = FormManageComment(request.form)
        obj_calification = Calification.load(document, reference)
        obj_calification_validate = Calification.edit(
            rating, form.comment.data, reference, obj_calification.id
        )
        obj_calification = Calification.load(document, reference)
        if obj_calification_validate:
            return render_template(
                "comments.html",
                form=FormManageComment(),
                option="Editar",
                calification=obj_calification,
                message="Editado correctamente",
                list_product_ser=Product.list_search(),
            )
        return render_template(
            "comments.html",
            form=FormManageComment(),
            option="Crear",
            error="No se pudo editar el comentario",
            list_product_ser=Product.list_search(),
        )


@app.route("/comentario/gestionar/eliminar/<id>")
def delete_comment(id):
    obj_calification = Calification.delete(id)
    if obj_calification:
        obj_calification += id
        return render_template(
            "comments.html",
            option="Crear",
            message="Borrado correctamente",
            list_products=Product.list_search(),
        )
    return render_template(
        "comments.html",
        form=FormManageComment(),
        option="Crear",
        error="No se pudo editar el comentario",
        list_product_ser=Product.list_search(),
    )


@app.route("/administrador/")
def admin():
    if request.method == "POST":
        create_user()
    return render_template(
        "admin.html",
        list_users=Person.listado("user"),
        formSearch=FormSearch(),
        list_product_ser=Product.list_search(),
    )


@app.route("/administrador/gestionar/Edit/<document>", methods=["GET", "POST"])
def edit_user(document):
    if request.method == "GET":
        formulario = FormManage()
        obj_user = Person.load("user", document)
        if obj_user:
            formulario.document.data = obj_user.document
            formulario.nickname.data = obj_user.nickname
            formulario.name.data = obj_user.name
            formulario.last_name.data = obj_user.last_name
            formulario.email.data = obj_user.email
            formulario.phone.data = obj_user.phone
            formulario.gender.data = obj_user.gender
            formulario.address.data = obj_user.address
            formulario.country.data = obj_user.country
            formulario.department.data = obj_user.department
            formulario.city.data = obj_user.city
            formulario.password.data = ""
            return render_template(
                "admin.html",
                User=obj_user,
                list_users=Person.listado("user"),
                option="Editar",
                form=formulario,
                formSearch=FormSearch(),
                list_products=Product.list_search(),
            )
        return render_template(
            "admin.html",
            error="No existe el User",
            list_users=Person.listado("user"),
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )
    else:
        formulario = FormManage(request.form)
        if formulario.validate_on_submit():
            obj_user = Person.editar(
                document,
                formulario.nickname.data,
                formulario.name.data,
                formulario.last_name.data,
                formulario.email.data,
                formulario.phone.data,
                formulario.gender.data,
                formulario.address.data,
                formulario.country.data,
                formulario.department.data,
                formulario.city.data,
                formulario.password.data,
                "user",
            )
            if obj_user:
                obj_user = obj_user = Person.load("user", document)
                return render_template(
                    "admin.html",
                    User=obj_user,
                    list_users=Person.listado("user"),
                    option="Editar",
                    form=FormManage(),
                    message="Se han editado los datos del usuario {0} {1} correctamente".format(
                        formulario.name.data, formulario.last_name.data
                    ),
                    formSearch=FormSearch(),
                    list_product_ser=Product.list_search(),
                )
        return render_template(
            "admin.html",
            list_users=Person.listado("user"),
            error="Verifique los datos ingresados",
            form=FormManage(),
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )


@app.route("/administrador/gestionar/buscar", methods=["GET", "POST"])
def search_user():
    if request.method == "GET":
        return render_template(
            "admin.html",
            list_users=Person.listado("user"),
            option="Editar",
            form=FormManage(),
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )
    else:
        form = FormSearch(request.form)
        formulario = FormManage()
        if form.validate_on_submit() or formulario.validate_on_submit():
            obj_user = Person.load("user", form.search.data)
            if obj_user:
                formulario.document.data = obj_user.document
                formulario.nickname.data = obj_user.nickname
                formulario.name.data = obj_user.name
                formulario.last_name.data = obj_user.last_name
                formulario.email.data = obj_user.email
                formulario.phone.data = obj_user.phone
                formulario.gender.data = obj_user.gender
                formulario.address.data = obj_user.address
                formulario.country.data = obj_user.country
                formulario.department.data = obj_user.department
                formulario.city.data = obj_user.city
                formulario.password.data = obj_user.password
                return render_template(
                    "admin.html",
                    User=obj_user,
                    list_users=Person.listado("user"),
                    option="Editar",
                    form=formulario,
                    formSearch=FormSearch(),
                    list_product_ser=Product.list_search(),
                )
            return render_template(
                "admin.html",
                list_users=Person.listado("user"),
                error="No existe el User, puede crearlo",
                option="crear",
                form=FormManage(),
                formSearch=FormSearch(),
                list_product_ser=Product.list_search(),
            )
        return render_template(
            "admin.html",
            list_users=Person.listado("user"),
            error="Error en el proceso de buscar User",
            option="Crear",
            form=FormManage(),
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )


@app.route("/administrador/gestionar/crear", methods=["GET", "POST"])
def create_user():
    if request.method == "GET":
        return render_template(
            "admin.html",
            list_users=Person.listado("user"),
            option="Crear",
            form=FormManage(),
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )
    else:
        formulario = FormManage(request.form)
        if formulario.validate_on_submit():
            obj_user = Person(
                formulario.document.data,
                formulario.nickname.data,
                formulario.name.data,
                formulario.last_name.data,
                formulario.email.data,
                formulario.phone.data,
                formulario.gender.data,
                formulario.address.data,
                formulario.country.data,
                formulario.department.data,
                formulario.city.data,
                formulario.password.data,
                "user",
                "T",
            )
            if obj_user.crear():
                return render_template(
                    "admin.html",
                    User=obj_user,
                    list_users=Person.listado("user"),
                    option="Editar",
                    form=FormManage(),
                    message="Creado correctamente el User " + formulario.nickname.data,
                    formSearch=FormSearch(),
                    list_product_ser=Product.list_search(),
                )
            return render_template(
                "admin.html",
                list_users=Person.listado("user"),
                error="El User con document "
                + formulario.document.data
                + " ya existe, o ingresó un campo erróneo",
                option="Editar",
                form=FormManage(),
                formSearch=FormSearch(),
                list_product_ser=Product.list_search(),
            )
        return render_template(
            "admin.html",
            list_users=Person.listado("user"),
            error="Error en el proceso de crear User, valide los campos ingresados",
            option="Editar",
            form=FormManage(),
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )


@app.route("/administrador/gestionar/Delete/<document>")
def delete_user(document):
    obj_user = Person.delete("user", document)
    if obj_user:
        obj_user += document
        return render_template(
            "admin.html",
            message=obj_user,
            list_users=Person.listado("user"),
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )
    return render_template(
        "admin.html",
        error="No se pudo eliminar al User " + document,
        list_users=Person.listado("user"),
        formSearch=FormSearch(),
        list_product_ser=Product.list_search(),
    )


@app.route("/administrador/gestionar/Block/<document><estado>")
def block_user(document, estado):
    obj_user = Person.block(document, estado)
    if obj_user:
        if estado == "T":
            obj_user = "Usuario " + document + " bloqueado "
        elif estado == "F":
            obj_user = "Usuario " + document + " desbloqueado "
        return render_template(
            "admin.html",
            message=obj_user,
            list_users=Person.listado("user"),
            block=estado,
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )
    return render_template(
        "admin.html",
        error="No se pudo bloquear al User",
        list_users=Person.listado("user"),
        formSearch=FormSearch(),
        list_product_ser=Product.list_search(),
    )


@app.route("/Products/<gender>/")
def list_products(gender):
    s = ""
    if gender == "HOMBRE":
        s = "M"
    if gender == "MUJER":
        s = "F"
    print(s)
    return render_template(
        "products.html",
        list_products_total=Product.list_reference(s),
        gender=gender,
        filter=FormFilterProduct(),
        list_product_ser=Product.list_search(),
    )


@app.route("/Products/<gender>/filters/", methods=["GET", "POST"])
def filter_product(gender):
    s = ""
    if gender == "HOMBRE":
        s = "M"
    if gender == "MUJER":
        s = "F"
    if request.method == "GET":
        return render_template(
            "products.html",
            list_products_total=Product.list_reference(s),
            gender=gender,
            filter=FormFilterProduct(),
            list_product_ser=Product.list_search(),
        )
    else:
        form = FormFilterProduct(request.form)
        if form.validate_on_submit():
            if (
                len(
                    Product.filter(
                        s,
                        form.orden.data,
                        form.size.data,
                        form.color.data,
                    )
                )
                > 0
            ):
                return render_template(
                    "products.html",
                    list_products_total=Product.filter(
                        s,
                        form.orden.data,
                        form.size.data,
                        form.color.data,
                    ),
                    gender=gender,
                    filter=FormFilterProduct(),
                    list_product_ser=Product.list_search(),
                )
            return render_template(
                "products.html",
                list_products_total=Product.list_reference(s),
                gender=gender,
                filter=FormFilterProduct(),
                error="No hay Products asociados a los filtros requeridos",
                list_product_ser=Product.list_search(),
            )

        return render_template(
            "products.html",
            list_products_total=Product.list_reference(s),
            gender=gender,
            filter=FormFilterProduct(),
            error="No hay Products asociados a los filtros requeridos",
            list_product_ser=Product.list_search(),
        )


@app.route("/Products/gestion/", methods=["GET", "POST"])
def management_products():
    return render_template(
        "management_products.html",
        list_products=Product.listado(),
        formSearch=FormSearch(),
        list_product_ser=Product.list_search(),
    )


@app.route("/Products/gestion/buscar", methods=["GET", "POST"])
def search_management_products():
    if request.method == "GET":
        return render_template(
            "management_products.html",
            list_products=Product.listado(),
            option="Editar",
            form=FormManagementProduct(),
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )
    else:
        form = FormSearch(request.form)
        if form.validate_on_submit():
            obj_product = Product.list_search_product(form.search.data)
            if obj_product:
                return render_template(
                    "management_products.html",
                    list_products=obj_product,
                    formSearch=FormSearch(),
                    list_product_ser=Product.list_search(),
                )
            return render_template(
                "management_products.html",
                list_products=Product.listado(),
                error="No existe el Product, puede crearlo",
                formSearch=FormSearch(),
                list_product_ser=Product.list_search(),
            )
        return render_template(
            "management_products.html",
            list_products=Product.listado(),
            error="Error en el proceso de buscar Product",
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )


@app.route("/Products/gestion/edit/BlockProducto=<reference><estado>")
def block_product(reference, estado):
    obj_state = Product.block(reference, estado)
    if obj_state:
        if estado == "T":
            obj_state = "Producto con " + reference + " bloqueado "
        elif estado == "F":
            obj_state = "Producto con " + reference + " desbloqueado "
        return render_template(
            "management_products.html",
            message=obj_state,
            list_products=Product.listado(),
            block=estado,
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )
    return render_template(
        "management_products.html",
        error="No se pudo bloquear al Product",
        list_products=Product.listado(),
        formSearch=FormSearch(),
        list_product_ser=Product.list_search(),
    )


@app.route("/Products/gestion/<id>", methods=["GET", "POST"])
def edit_product(id):
    if request.method == "GET":
        formulario = FormManagementProduct()
        obj_mensaje = Product.cargar(id)
        if obj_mensaje:
            formulario.name.data = obj_mensaje.name
            formulario.reference.data = obj_mensaje.reference
            formulario.size.data = obj_mensaje.size
            formulario.price.data = obj_mensaje.price
            formulario.amount.data = obj_mensaje.amount
            formulario.discount.data = obj_mensaje.discount
            formulario.color.data = obj_mensaje.color
            formulario.description.data = obj_mensaje.description
            formulario.gender.data = obj_mensaje.gender
            return render_template(
                "management_products.html",
                Product=obj_mensaje,
                list_products=Product.listado(),
                option="Editar",
                form=formulario,
                formSearch=FormSearch(),
                list_product_ser=Product.list_search(),
            )
        return render_template(
            "management_products.html",
            error="No existe el Product",
            list_products=Product.listado(),
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )
    else:
        formulario = FormManagementProduct(request.form)
        if formulario.validate_on_submit():
            obj_user = Product.editar(
                id,
                formulario.name.data,
                formulario.reference.data,
                formulario.size.data,
                formulario.price.data,
                formulario.amount.data,
                formulario.discount.data,
                formulario.color.data,
                formulario.description.data,
                formulario.gender.data,
            )
            if obj_user:
                obj_user = Product.cargar(id)
                return render_template(
                    "management_products.html",
                    Product=obj_user,
                    list_products=Product.listado(),
                    option="Editar",
                    form=FormManagementProduct(),
                    message="Editado correctamente",
                    formSearch=FormSearch(),
                    list_product_ser=Product.list_search(),
                )
        return render_template(
            "management_products.html",
            list_products=Product.listado(),
            error="Verifique los datos ingresados",
            form=FormManagementProduct(),
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )


@app.route("/Products/gestion/crear", methods=["GET", "POST"])
def create_product():
    if request.method == "GET":
        formulario = FormManagementProduct()
        return render_template(
            "management_products.html",
            list_products=Product.listado(),
            option="Crear",
            form=formulario,
            list_product_ser=Product.list_search(),
        )
    else:
        formulario = FormManagementProduct(request.form)
        if formulario.validate_on_submit():
            obj_create_product = Product(
                "",
                formulario.name.data,
                formulario.reference.data,
                formulario.size.data,
                formulario.price.data,
                formulario.amount.data,
                formulario.discount.data,
                formulario.color.data,
                formulario.description.data,
                formulario.gender.data,
                list_products=Product.list_search(),
            )
            if obj_create_product.crear():
                return render_template(
                    "management_products.html",
                    Product=obj_create_product,
                    list_products=Product.list(),
                    option="Editar",
                    form=FormManagementProduct(),
                    message="Creado correctamente el producto " + formulario.name.data,
                    formSearch=FormSearch(),
                    list_product_ser=Product.list_search(),
                )

            return render_template(
                "management_products.html",
                list_products=Product.listado(),
                error="Error en el proceso de crear Product",
                option="Crear",
                form=FormManagementProduct(),
                formSearch=FormSearch(),
                list_product_ser=Product.list_search(),
            )
        return render_template(
            "management_products.html",
            list_products=Product.listado(),
            error="Error en el proceso de crear Product",
            option="Crear",
            form=FormManagementProduct(),
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )


@app.route("/Products/gestion/Delete/<id>")
def delete_product(id):
    obj_user = Product.delete(id)
    if obj_user:
        obj_user += id
        return render_template(
            "management_products.html",
            message=obj_user,
            list_products=Product.listado(),
            formSearch=FormSearch(),
            list_product_ser=Product.list_search(),
        )
    return render_template(
        "management_products.html",
        error="No se pudo eliminar al Product " + id,
        list_products=Product.listado(),
        formSearch=FormSearch(),
        list_product_ser=Product.list_search(),
    )


@app.route("/gestion/micuenta/<document>", methods=["GET", "POST"])
def management_my_account(document):
    if request.method == "GET":
        formulario = FormMyAccount()
        obj_user = Account.load(document)
        if obj_user:
            formulario.name.data = obj_user.name
            formulario.last_name.data = obj_user.last_name
            formulario.document.data = obj_user.document
            formulario.gender.data = obj_user.gender
            formulario.nickname.data = obj_user.nickname
            formulario.phone.data = obj_user.phone
            formulario.email.data = obj_user.email
            formulario.country.data = obj_user.country
            formulario.department.data = obj_user.department
            formulario.city.data = obj_user.city
            formulario.address.data = obj_user.address
            formulario.password.data = ""
            formulario.new_password.data = ""
            formulario.confirm_new_password.data = ""
            return render_template(
                "account.html",
                datosUsuario=obj_user,
                form=formulario,
                document=document,
                list_product_ser=Product.list_search(),
            )
        return render_template(
            "account.html",
            error="No existe el User",
            form=formulario,
            list_product_ser=Product.list_search(),
        )
    else:
        formulario = FormMyAccount(request.form)
        if formulario.validate_on_submit:
            obj_user = Account.load(document)

            if obj_user:
                obj_logging = User(
                    formulario.nickname.data,
                    formulario.document.data,
                    formulario.email.data,
                    formulario.password.data,
                    "",
                )
                if obj_logging.logging():
                    obj_user.name = formulario.name.data
                    obj_user.last_name = formulario.last_name.data
                    obj_user.document = formulario.document.data
                    obj_user.gender = formulario.gender.data
                    obj_user.nickname = formulario.nickname.data
                    obj_user.phone = formulario.phone.data
                    obj_user.email = formulario.email.data
                    obj_user.country = formulario.country.data
                    obj_user.department = formulario.department.data
                    obj_user.city = formulario.city.data
                    obj_user.address = formulario.address.data
                    if len(formulario.new_password.data) > 0:
                        obj_user.password = formulario.new_password.data
                    else:
                        obj_user.password = formulario.password.data
                    obj_user.editar_datos()
                    return render_template(
                        "account.html",
                        datosUsuario=obj_user,
                        form=formulario,
                        message="Se han editado correctamente los datos",
                        list_product_ser=Product.list_search(),
                    )

            return render_template(
                "account.html",
                datosUsuario=obj_user,
                form=formulario,
                error="Error en el proceso de edición de los datos",
            )

    return render_template(
        "account.html",
        form=FormMyAccount(),
        list_product_ser=Product.list_search(),
    )


@app.route("/superadministrador/")
def super_admin():
    return render_template(
        "super_admin.html",
        formSearch=FormSearchAdmin(),
        list_admin=Admin.list(),
        list_product_ser=Product.list_search(),
    )


@app.route("/superadministrador/gestionar/<document>", methods=["GET", "POST"])
def edit_admin(document):
    if request.method == "GET":
        form = FormManage()
        obj_admin = Admin.load(document)
        if obj_admin:
            form.name.data = obj_admin.nombre
            form.last_name.data = obj_admin.apellido
            form.document.data = obj_admin.document
            form.gender.data = obj_admin.gender
            form.nickname.data = obj_admin.nickname
            form.phone.data = obj_admin.phone
            form.email.data = obj_admin.email
            form.country.data = obj_admin.country
            form.department.data = obj_admin.department
            form.city.data = obj_admin.city
            form.address.data = obj_admin.address
            form.password.data = ""
            form.confirm_password.data = ""
            return render_template(
                "super_admin.html",
                data_admin=obj_admin,
                form=form,
                formSearch=FormSearchAdmin(),
                list_admin=Admin.list(),
                option="Editar",
                list_product_ser=Product.list_search(),
            )
        return render_template(
            "super_admin.html",
            error="No existe el User",
            formSearch=FormSearchAdmin(),
            list_admin=Admin.list(),
            list_product_ser=Product.list_search(),
        )
    else:
        form = FormManage(request.form)
        if form.validate_on_submit():
            obj_admin = Admin.load(document)
            if obj_admin:
                obj_admin.name = form.name.data
                obj_admin.last_name = form.last_name.data
                obj_admin.gender = form.gender.data
                obj_admin.nickname = form.nickname.data
                obj_admin.phone = form.phone.data
                obj_admin.email = form.email.data
                obj_admin.country = form.country.data
                obj_admin.department = form.department.data
                obj_admin.city = form.city.data
                obj_admin.address = form.address.data
                obj_admin.password = form.password.data
                obj_admin.edit()
                return render_template(
                    "super_admin.html",
                    data_admin=obj_admin,
                    formSearch=FormSearchAdmin(),
                    list_admin=Admin.list(),
                    message="Se han editado los datos del administrador {0} {1} correctamente".format(
                        form.name.data, form.last_name.data
                    ),
                    option="Editar",
                    list_product_ser=Product.list_search(),
                )
        return render_template(
            "super_admin.html",
            form=FormManage(),
            formSearch=FormSearchAdmin(),
            list_admin=Admin.list(),
            error="Verifique los datos ingresados",
            list_product_ser=Product.list_search(),
        )


@app.route("/superadministrador/crear/", methods=["GET", "POST"])
def create_admin():
    if request.method == "GET":
        form = FormManage()
        return render_template(
            "super_admin.html",
            form=form,
            list_admin=Admin.list(),
            formSearch=FormSearchAdmin(),
            option="Crear",
            list_product_ser=Product.list_search(),
        )
    else:
        form = FormManage(request.form)
        if form.validate_on_submit():
            obj_admin = Admin(
                form.name.data,
                form.last_name.data,
                form.document.data,
                form.gender.data,
                form.nickname.data,
                form.phone.data,
                form.email.data,
                form.country.data,
                form.department.data,
                form.city.data,
                form.address.data,
                form.password.data,
                "admin",
                "T",
            )
            if obj_admin.create():
                return render_template(
                    "super_admin.html",
                    message="Se ha creado correctamente el administrador {0} {1} correctamente".format(
                        form.name.data, form.last_name.data
                    ),
                    list_admin=Admin.list(),
                    formSearch=FormSearchAdmin(),
                    option="Editar",
                    data_admin=obj_admin,
                    form=FormManage(),
                    list_product_ser=Product.list_search(),
                )
        return render_template(
            "super_admin.html",
            error="Error en el proceso de creación del administrador",
            form=FormManage(),
            list_admin=Admin.list(),
            formSearch=FormSearchAdmin(),
            option="Crear",
            list_product_ser=Product.list_search(),
        )


@app.route("/superadministrador/eliminar/<document>")
def delete_admin(document):
    obj_admin = Admin.load
    if obj_admin.delete():
        return render_template(
            "super_admin.html",
            message="Se ha eliminado correctamente el administrador {0}".format(
                document
            ),
            list_admin=Admin.list(),
            formSearch=FormSearchAdmin(),
            list_product_ser=Product.list_search(),
        )
    return render_template(
        "super_admin.html",
        error="Error en la eliminación del administrador",
        list_admin=Admin.list(),
        formSearch=FormSearchAdmin(),
        list_product_ser=Product.list_search(),
    )


@app.route("/superadministrador/bloquear/<document>")
def block_admin(document):
    obj_admin = Admin.load(document)
    obj_admin.block()
    if obj_admin.estado == "F":
        return render_template(
            "super_admin.html",
            message="Se ha desbloqueado el administrador {0}".format(document),
            list_admin=Admin.list(),
            formSearch=FormSearchAdmin(),
            list_product_ser=Product.list_search(),
        )
    elif obj_admin.estado == "T":
        return render_template(
            "super_admin.html",
            message="Se ha bloqueado el administrador {0}".format(document),
            list_admin=Admin.list(),
            formSearch=FormSearchAdmin(),
            list_product_ser=Product.list_search(),
        )
    return render_template(
        "super_admin.html",
        message="No se ha podido cambiar el estado del administrador {0}".format(
            document
        ),
        list_admin=Admin.list(),
        formSearch=FormSearchAdmin(),
        list_product_ser=Product.list_search(),
    )


@app.route("/superadministrador/buscar/", methods=["GET", "POST"])
def search_admin():
    if request.method == "GET":
        return render_template(
            "super_admin.html",
            list_admin=Admin.list(),
            formSearch=FormSearchAdmin(),
            form=FormManage(),
            list_product_ser=Product.list_search(),
        )
    else:
        form_search = FormSearchAdmin(request.form)
        formulario = FormManage()
        if form_search.validate_on_submit():
            obj_admin = Admin.load(form_search.search.data)
            if obj_admin:
                formulario.name.data = obj_admin.ame
                formulario.last_name.data = obj_admin.last_name
                formulario.document.data = obj_admin.document
                formulario.gender.data = obj_admin.gender
                formulario.nickname.data = obj_admin.nickname
                formulario.phone.data = obj_admin.phone
                formulario.email.data = obj_admin.email
                formulario.country.data = obj_admin.country
                formulario.department.data = obj_admin.department
                formulario.city.data = obj_admin.city
                formulario.address.data = obj_admin.address
                formulario.password.data = ""
                return render_template(
                    "super_admin.html",
                    data_admin=obj_admin,
                    form=formulario,
                    formSearch=FormSearchAdmin(),
                    list_admin=Admin.list(),
                    option="Editar",
                    list_products=Product.list_search(),
                    list_product_ser=Product.list_search(),
                )
            return render_template(
                "super_admin.html",
                form=formulario,
                formSearch=FormSearchAdmin(),
                list_admin=Admin.list(),
                option="Crear",
                error="No existe el administrador {o}, puede crearlo".format(
                    form_search.search.data
                ),
                list_product_ser=Product.list_search(),
            )
        return render_template(
            "super_admin.html",
            form=formulario,
            formSearch=FormSearchAdmin(),
            list_admin=Admin.list(),
            option="Crear",
            error="Error en el proceso de búsqueda",
            list_product_ser=Product.list_search(),
        )


@app.route("/comentarios/")
def all_comments():
    return render_template("all_comments.html", list_product_ser=Product.list_search())


@app.route("/contactos/")
def contacts():
    return render_template("contact.html", list_product_ser=Product.list_search())


@app.route("/linkedinInri")
def inri():
    return redirect("https://www.linkedin.com/in/stivenas")


@app.route("/linkedinJulian")
def julian():
    return redirect("https://www.linkedin.com/in/julianga/")


@app.route("/linkedinRau")
def raul():
    return redirect(
        "https://www.linkedin.com/in/raúl-andres-castaño-castellar-41b75bb3/"
    )


@app.route("/linkedinDavid")
def david():
    return redirect(
        "https://www.linkedin.com/in/david-daniel-hernandez-molina-98aab920a/"
    )


@app.route("/linkedinMajo")
def majo():
    return redirect(
        "https://www.linkedin.com/in/mar%C3%ADa-jos%C3%A9-sierra-jim%C3%A9nez-3582a99a/"
    )
