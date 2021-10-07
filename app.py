from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index')
def hola_mundo():
    return render_template('index.html') 