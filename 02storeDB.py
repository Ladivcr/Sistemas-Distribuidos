#!/usr/bin/env python3
import mysql.connector
from mysql.connector import errorcode
import json
import glob, os
import xml.etree.ElementTree as ET
import mysql.connector
from mysql.connector import errorcode
import datetime
import subprocess



#PATH = '/home/galimatias/public_html/static/'

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
  print("Conexión exitosa!")
  
  
  
  
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print("Error: ",err)
    
else:
  cnx.close()
  print("Base de datos cerrada exitosamente")
