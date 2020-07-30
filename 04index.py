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
    try:
        cnx = mysql.connector.connect(user=userDB, password=passwordDB, host=hostDB, database=nameDB)
        print("Conexión exitosa!\n")
        cursor = cnx.cursor()
        query = ("SELECT hashtag, quantity, publication_date FROM possible_trends ORDER BY quantity DESC;")
        #query2 = ("SELECT hashtag, quantity, publication_date FROM possible_trends WHERE quantity = (SELECT MAX(quantity) FROM possible_trends);")
        cursor.execute(query)
        #cursor2.execute(query2)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("Error: ",err)

    mydata = []
    #datos = cursor.fetchall()

    for (hashtag, quantity, date) in cursor:
        #mydata2[hashtag]=[quantity, str(date)]
        mydata.append([hashtag, quantity, str(date)])

    print(mydata[0])
    return render_template("index.html", maxData = mydata[0])

@app.route("/historial-tendencias")
def graph_page():
    #mydata2 = {}
    try:
        cnx = mysql.connector.connect(user=userDB, password=passwordDB, host=hostDB, database=nameDB)
        print("Conexión exitosa!\n")
        cursor = cnx.cursor()
        query = ("SELECT hashtag, quantity, publication_date FROM possible_trends ORDER BY quantity DESC;")
        #query2 = ("SELECT hashtag, quantity, publication_date FROM possible_trends WHERE quantity = (SELECT MAX(quantity) FROM possible_trends);")
        cursor.execute(query)
        #cursor2.execute(query2)

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print("Error: ",err)

    contador = 0
    mydata = []
    #datos = cursor.fetchall()

    for (hashtag, quantity, date) in cursor:
        #mydata2[hashtag]=[quantity, str(date)]
        mydata.append([hashtag, quantity, str(date)])
        contador += 1
        if contador == 9:
            break

    return render_template('historial.html', dataSet = mydata)

@app.route("/filterHashtag", methods = ['POST'])
def filterHashtag():
    uniqueH = request.form['filter']
    try:
        cnx = mysql.connector.connect(user=userDB, password=passwordDB, host=hostDB, database=nameDB)
        print("Conexión exitosa!\n")
        cursor = cnx.cursor()
        query = ("SELECT hashtag, quantity, publication_date FROM possible_trends WHERE hashtag = %s;")
        cursor.execute(query, (uniqueH,))
        cursor.fetchone()
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print("Error: ",err)

    #mydata = {}
    mydata = []
    for (hashtag, quantity, date) in cursor:
        #mydata[hashtag]=[quantity, str(date)]
        mydata.append([hashtag, quantity, str(date)])
    return render_template('historial.html', dataSet = mydata)

@app.route("/displayHashtag", methods = ['POST'])
def displayHashtag():
    values = request.form['values']
    inicio, fin = values.split(",")
    inicio = int(inicio); fin = int(fin)
    button = request.form['submit_button']

    try:
        cnx = mysql.connector.connect(user=userDB, password=passwordDB, host=hostDB, database=nameDB)
        print("Conexión exitosa!\n")
        cursor = cnx.cursor()
        query = ("SELECT hashtag, quantity, publication_date FROM possible_trends ORDER BY quantity DESC;")
        cursor.execute(query)

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print("Error: ",err)

    #mydata = {}
    mydata = []
    for (hashtag, quantity, date) in cursor:
        #mydata[hashtag]=[quantity, str(date)]
        mydata.append([hashtag, quantity, str(date)])

    aux = []
    for value in range(inicio, fin, 1):
        aux.append(mydata[value])

    # Tengo que desplegar dado un cierto rango
    return render_template('historial.html', dataSet = aux)

# Función principal
if __name__ == "__main__":
    # Ejecutamos el objeto
    app.run(debug=True)
