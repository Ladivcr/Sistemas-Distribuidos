# Importamos la librería
from flask import Flask, render_template
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





@app.route("/historial_trends")
def graph_page():
    return render_template('historial.html')




# Función principal
if __name__ == "__main__":
    # Ejecutamos el objeto
    app.run(debug=True)
