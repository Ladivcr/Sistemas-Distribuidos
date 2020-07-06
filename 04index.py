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
    """
    try:
      cnx = mysql.connector.connect(user=userDB, password=passwordDB, host=hostDB, database=nameDB)
      print("Conexión exitosa!\n")
      cursor = cnx.cursor()
      query = ("SELECT * FROM possible_trends")
      cursor.execute(query)
      Hashtags = cursor.fetchall()
      cnx.commit()
      hashtag = [x[0] for x in Hashtags]
      quantity = [x[1] for x in Hashtags]
      publication_date = [x[2] for x in Hashtags]

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print("Error: ",err)

    else:
      cnx.close()
    """
    return render_template('historial.html')




# Función principal
#if __name__ == "__main__":
    # Ejecutamos el objeto
    #app.run(debug=True)
