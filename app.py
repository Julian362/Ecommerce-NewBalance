from flask import Flask, render_template

app = Flask(__name__)

""" @app.route('/template')
def hola_mundo():
    return render_template('template.html') """

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/registro/')
def registro():
    return render_template('registro.html')

@app.route('/gestioncomentario/')
def gestioncomentario():
    return render_template('gestion_comentario.html')

@app.route('/administrador/')
def administrador():
    return render_template('administrador.html')

@app.route('/')
def index():
    return render_template('index.html')

"""Ruta para llamar a los productos de hombre"""
@app.route('/productos_hombre/')
def lista_de_productos_hombre():
    return render_template('productos_hombre.html')

"""Ruta para llamar a los productos de mujer"""
@app.route('/productos_mujer/')
def lista_de_productos_mujer():
    return render_template('productos_mujer.html')

@app.route('/gestion_productos/')
def gestion_productos():
    return render_template('gestion_productos.html')
    
"""Ruta para la gestión de perfil (Mi Cuenta)"""
@app.route('/gestion_micuenta/')
def gestion_micuenta():
    return render_template('gestion_micuenta.html')

"""Ruta para la gestión de Superadministrador"""
@app.route('/superadministrador/')
def superadministrador():
    return render_template('superadministrador.html')

"""Ruta para todos los comentarios de un producto"""
@app.route('/todos_los_comentario/')
def todos_los_comentarios():
    return render_template('todos_los_comentarios.html')

@app.route('/contactos/')
def contactos():
    return render_template('contactos.html')
