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

"""Ruta para llamar a los productos de hombre"""
@app.route('/productos_hombre/')
def lista_de_productos_hombre():
    return render_template('lista_de_productos.html')

"""Ruta para llamar a los productos de mujer"""
@app.route('/productos_mujer/')
def lista_de_productos_mujer():
    return render_template('lista_de_productos.html')

@app.route('/')
def index():
    return render_template('index.html')
