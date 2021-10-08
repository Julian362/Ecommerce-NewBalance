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
@app.route('/')
def index():
    return render_template('index.html')
