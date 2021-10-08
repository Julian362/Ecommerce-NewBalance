from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
def hola_mundo():
    return render_template('index.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/registro/')
def registro():
    return render_template('registro.html')