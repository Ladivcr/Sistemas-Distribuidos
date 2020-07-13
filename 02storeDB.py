#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
@uthor: José Vidal Cardona Rosas
About: Store the information that we get from twitter.
"""

import mysql.connector
from mysql.connector import errorcode
import json
import glob
import os
import datetime
import subprocess
import fnmatch
import sys


#PATH = '/home/galimatias/public_html/static/'
#PATH de trabajo
PATH='/home/ladiv/github/Sistemas-Distribuidos/tweets'
#PATH para respaldo
#RPATH = '/home/ladiv/git/Sistemas-Distribuidos/json/backup'

# Cargamos las credenciales
with open('credentialsDB.json') as file:
    credentials = json.load(file)

# Seleccionamos las credenciales
userDB = credentials["credentials"][0]["user"]
passwordDB = credentials["credentials"][0]["password"]
hostDB = credentials["credentials"][0]["host"]
nameDB = credentials["credentials"][0]["database"]


try:
  cnx = mysql.connector.connect(user=userDB, password=passwordDB, host=hostDB, database=nameDB)
  print("Conexión exitosa!\n")
  cursor = cnx.cursor()
  query = ("INSERT INTO possible_trends(hashtag, quantity, publication_date) VALUES(%s, %s, %s)")

  # Leemos los archivos json en nuestro directorio
  files = os.listdir(PATH)
  for x in files:
      archivo = open(PATH+"/"+x, 'r')
      #myFile = archivo.read()
      myFile = json.load(archivo)

      for key, value in myFile.items():
          #print(key, value[0])
          hashtag = key; quantity = value[0]; publication_date = value[1]
          data_query = (hashtag, quantity, publication_date)
          cursor.execute(query,data_query)
          cnx.commit()

   print("Querys efectuadas correctamente...")


  #Cerramos el programa para que el sh pueda ejecutar el siguiente
  #sys.exit()

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print("Error: ",err)

else:
  cnx.close()
  #print("\nConexión cerrada exitosamente!\nNo a sido posible almacenar los datos...")
