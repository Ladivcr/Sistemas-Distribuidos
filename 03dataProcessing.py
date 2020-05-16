#!/usr/bin/env python3
"""
 Execute a query to the database, 
 process information and produces
 a simple plot with a possible trend.
"""
import mysql.connector
from mysql.connector import errorcode
import json
import glob
import datetime
import subprocess
import matplotlib
#matplotlib.use('Agg') #Usamos el ambiente gráfico del sistema
import matplotlib.pyplot as plt
import sys


#PATH='/home/galimatias/public_html/static/'

# Cargamos las credenciales
with open('credentialsDB.json') as file:
    credentials = json.load(file)    

# Seleccionamos las credenciales
userDB = credentials["credentials"][0]["user"]
passwordDB = credentials["credentials"][0]["password"]
hostDB = credentials["credentials"][0]["host"]
nameDB = credentials["credentials"][0]["database"]

# Creamos los vectores para graficar
x = []; y = []
try:
  cnx = mysql.connector.connect(user=userDB, password=passwordDB, host=hostDB, database=nameDB)
  print("Conexión exitosa!\n")
  cursor = cnx.cursor()
  query = ("SELECT hashtag, quantity FROM possible_trends WHERE quantity > 50 ORDER BY quantity")
  cursor.execute(query)
  for (hashtag, quantity) in cursor:
      print(f"{hashtag}\t{quantity}")
      x.append(hashtag)
      y.append(quantity)

  
        
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()

# Graficar
fig, ax = plt.subplots()
now = datetime.datetime.now()
actual_date = now.strftime('Day :%d, Month: %m, Year: %Y, Hour: %H, Minutes: %M, Seconds: %S')
ax.set(xlabel='Tags', ylabel='Number of tweets', title=actual_date)
font = {'family' : 'normal', 'weight' : 'normal', 'size'   : 8}
arr_temp = [int(i) for i in range(len(x))] # arreglo temporal para el eje x 
ax.plot(arr_temp, y, "-or")
ax.grid()
# Establecer el tamaño de los ejes
plt.ylim(0, max(y)+5)
plt.yscale("linear")
# Etiquetar los puntos
for label, xx, yy in zip(x, arr_temp, y):
    plt.annotate(label, xy=(xx, yy), xytext=(-15, 15),textcoords='offset points', ha='right', va='bottom',
                 bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),arrowprops=dict(arrowstyle = '->',
                                                                                             connectionstyle='arc3,rad=0'))
                
         
# Guardamos la gráfica 
#today = datetime.datetime.now()
#día-mes-año - horas-minutos-segundos
actual_day = now.strftime('/home/ladiv/github/Sistemas-Distribuidos/graphics/possible_trends-%d-%m-%Y-%H-%M-%S.png')
plt.savefig(actual_day, bbox_inches='tight')
#plt.show()
sys.exit()

#NOTA PARA EL AUTOR: Necesito borrar cada día los registros realizados en la base de datos 
#Ya que las tendencias son por días por lo que no vale la pena guardarlas más de un día. 
