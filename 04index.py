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
    mydata = {}
    cnx = mysql.connector.connect(user=userDB, password=passwordDB, host=hostDB, database=nameDB)
    print("Conexión exitosa!\n")
    cursor = cnx.cursor()
    query = ("SELECT hashtag, quantity, publication_date FROM possible_trends;")
    cursor.execute(query)
    for (hashtag, quantity, date) in cursor:
        mydata[hashtag]=[quantity, str(date)]

    return render_template('historial.html', dataSet = mydata)


@app.route("/filterHashtag", methods = ['POST', 'GET'])
def filterHashtag():
    uniqueH = request.form['filter']
    cnx = mysql.connector.connect(user=userDB, password=passwordDB, host=hostDB, database=nameDB)
    print("Conexión exitosa!\n")
    cursor = cnx.cursor()
    query = ("SELECT hashtag, quantity, publication_date FROM possible_trends WHERE hashtag = %s;")
    cursor.execute(query, (uniqueH))
    mydata = cursor.fetchall()
    for x in mydata:
        print (x)



# Función principal
if __name__ == "__main__":
    # Ejecutamos el objeto
    app.run(debug=True)
