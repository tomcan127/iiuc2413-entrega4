﻿from flask import Flask, render_template, request, abort, json, jsonify
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

USER_KEYS = ['name', 'last_name', 'occupation', 'follows', 'age']

# El cliente se levanta en la URL de la wiki
uri = "mongodb://grupo15:grupo15@gray.ing.puc.cl/grupo15"
# La uri 'estándar' es "mongodb://user:password@ip/database"
client = MongoClient(uri)
db = client.get_database()

# Iniciamos la aplicación de flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>HELLO</h1>"

# Mapeamos esta función a la ruta '/plot' con el método get.
@app.route("/plot")
def plot():
    # Export la figura para usarla en el html
    pth = os.path.join('static', 'plot.png')

    # Retorna un html "rendereado"
    return render_template('plot.html')

@app.route("/messages")
def get_users():
    # Omitir el _id porque no es json serializable
    resultados = db.messages.find()
    return resultados[0]["content"]

@app.route("/users", methods=['POST'])
def create_user():
    '''
    Crea un nuevo usuario en la base de datos
    Se  necesitan todos los atributos de model, a excepcion de _id
    '''
    return json.jsonify({'success': True, 'message': 'Usuario con id 1 creado'})

@app.route("/test")
def test():
    # Obtener un parámero de la URL
    param = request.args.get('name', False)
    print("URL param:", param)

    # Obtener un header
    param2 = request.headers.get('name', False)
    print("Header:", param2)

    # Obtener el body
    body = request.data
    print("Body:", body)

    return "OK"


@app.route('/saludo', methods=['GET'])
def formulario():
    # Comprobamos si viene el parametro por GET
    try:
        content = request.args.get('content')

        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        time = dt_string

        sender = request.args.get('sender')
        receiver = request.args.get('receiver')
        if (content != '' and sender != '' and receiver != '' ):
            return db.messages.find()
        else:
            return render_template('formulario_get.html')
    except:
        return render_template('formulario_get.html')

@app.route('/messages/<id>', methods=['GET'])
def my_view_func(id):
    return id

if __name__ == "__main__":
    app.run()


