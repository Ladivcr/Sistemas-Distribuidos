#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
@uthor: José Vidal Cardona Rosas
About: Work in back-end for the control of web page
"""
# Importamos la librería
from flask import Flask, render_template, request
import json
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from mysql.connector import errorcode
# Cargamos las credenciales
with open('credentialsDB.json') as file:
    credentials = json.load(file)

# Seleccionamos las credenciales
userDB = credentials["credentials"][0]["user"]
passwordDB = credentials["credentials"][0]["password"]
hostDB = credentials["credentials"][0]["host"]
nameDB = credentials["credentials"][0]["database"]

# Creamos el objeto de flask que nos servira para lanzar el servidor
# y la página web
app = Flask(__name__)

#Indicamos la ruta para la página principal, que corresponde a la ruta donde
# nosotros estamos corriendo el archivo
@app.route("/")
# Definimos la función para la ruta de la página principal
def index():
    return render_template("index.html")

@app.route("/historial-tendencias")
def graph_page():
    #mydata2 = {}
    try:
        cnx = mysql.connector.connect(user=userDB, password=passwordDB, host=hostDB, database=nameDB)
        print("Conexión exitosa!\n")
        cursor = cnx.cursor()
        query = ("SELECT hashtag, quantity, publication_date FROM possible_trends;")
        cursor.execute(query)
    except:
        print("No a sido posible establecer conexión/hacer la consulta")

    contador = 0
    mydata = []
    #datos = cursor.fetchall()

    for (hashtag, quantity, date) in cursor:
        #mydata2[hashtag]=[quantity, str(date)]
        mydata.append([hashtag, quantity, str(date)])
        contador += 1
        if contador == 8:
            break

            #print(mydata2)
    return render_template('historial.html', dataSet = mydata)

@app.route("/filterHashtag", methods = ['POST', 'GET'])
def filterHashtag():
    uniqueH = request.form['filter']
    try:
        cnx = mysql.connector.connect(user=userDB, password=passwordDB, host=hostDB, database=nameDB)
        print("Conexión exitosa!\n")
        cursor = cnx.cursor()
        query = ("SELECT hashtag, quantity, publication_date FROM possible_trends WHERE hashtag = %s;")
        cursor.execute(query, (uniqueH,))
        cursor.fetchone()
    except:
        print("No a sido posible establecer conexión/realizar la consulta")

    #mydata = {}
    mydata = []
    for (hashtag, quantity, date) in cursor:
        #mydata[hashtag]=[quantity, str(date)]
        mydata.append([hashtag, quantity, str(date)])
    return render_template('historial.html', dataSet = mydata)


# Función principal
if __name__ == "__main__":
    # Ejecutamos el objeto
    app.run(debug=True)
