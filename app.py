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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/producto/')
def productoind():
    return render_template('ProductoIndividual.html')

@app.route('/carrito/')
def carrito():
    return render_template('Carrito.html')