#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
@uthor: José Vidal Cardona Rosas
About: Get information from Twitter, precisely from Tweets.
"""

import tweepy
#import twitter
import json
import requests
import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import time
import subprocess


# Tiempo para el control de la recepción de tuits (esta en segundos)
start_time = time.time()
# Diccionario para controlar el número de hashtags
hashtags = {}
# Lista para guardar el tiempo en el que el tuit fue publicado
time_vector = []
# Lista para guardar los hashtags
tag_vector = []
# Control de las ejecuciones de código
saveValues = []
# Cargamos las credenciales
with open('credentials.json') as file:
    credentials = json.load(file)

# Seleccionamos las credenciales
api_key = credentials["credentials"][0]["api_key"]
api_secret_key = credentials["credentials"][0]["api_secret_key"]
access_token = credentials["credentials"][0]["access_token"]
access_token_secret = credentials["credentials"][0]["access_token_secret"]

try:
    # Nos autenticamos con nuestras credenciales de twitter
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    # WAIT ON RATE LIMIT Nos garantiza que al llegar a un limite el código no caiga
    # sino que espera hasta volver a tener cota
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

except:
    print("Error en la verificación, revisa las credenciales")

# Creamos una clase para monitorear los tuits
class TweetsListener(tweepy.StreamListener):

    # Efectuamos la conexión
    def on_connect(self):
        print("Conexión exitosa!")



    # Método para recibir los tuits
    def on_status(self, status):
        #print(start_time)
        #print(status.text) # Texto del tuit
        publication_date = str(status.created_at) # Convertimos el tipo de dato de la fecha en string
        response = {"hashtags":status.entities["hashtags"], "publication_date":publication_date, "coordinates":status.coordinates}


        # Convertimos los atributos con los que vamos a trabajar en un dato del tipo JSON
        data = json.dumps(response)

        # Cargamos los datos ahora como un tipo de dato JSON
        data = json.loads(data)

        hasht = list(data["hashtags"]) #Obtenemos los hashtags del tuit
        # Hacemos un recorrido por los hashtags y comparamos con nuestro diccionario de hashtags
        if len(hasht) != 0:
            print(status.text)
            for dicci in hasht:
                tag = dicci["text"]
                tag = tag.lower()
                tag = str(tag) # agregue esto para lidiar con un problema en strings
                #print(tag)
                if (tag in hashtags.keys()) == True:
                    hashtags[tag][0] += 1
                else:
                    #print("entre")

                    date = data["publication_date"] # obtener la fecha
                    #print(date)
                    hashtags[tag] = [1, date]
                    date = date.split(" ")
                    hour = date[1]
                    today = date[0]
                    time_vector.append(hour)
                    tag_vector.append(tag)


        # Conteo del tiempo transcurrido
        elapsed_time = time.time() - start_time # Obtenemos el tiempo transcurrido
        elapsed_time_seg = int(elapsed_time) # Obtenemos los segundos

        # Guardaremos los datos cada 10 minutos (Falta averiguar como reiniciar el conteo del reloj) - NOTA Para mi
        #print(elapsed_time)
        # Debo de modificar esta instruccion sino el programa se correra esto monton de veces cuando se
        # alcance el umbral de tiempo

        if elapsed_time_seg >= 680:

            # Guardar los tuits
            myJSON = json.dumps(hashtags)
            now = datetime.datetime.now()
            #día-mes-año - horas-minutos-segundos
            # Para un mejor orden de almacenamiento, nos basaremos
            # en la cantidad de archivos existentes
            PATH='/home/vdelaluz/git/Sistemas-Distribuidos/tweets'
            # Leemos los archivos json en nuestro directorio
            files = os.listdir(PATH)
            controlador = (len(files))+1
            filename = now.strftime('tweets/{0}-possible_trend-%d-%m-%Y-%H-%M.json'.format(controlador))
            #filename = now.strftime('tweets/possible_trend-%d-%m-%Y-%H-%M.json')

            #filename = str(controlador)+'-'+filename
            # Guardamos nuestros datos en un archivo json
            with open(filename,"w") as file:
                file.write(myJSON)

            file.close()
            try:
                os.system('python3 /home/vdelaluz/git/Sistemas-Distribuidos/02storeDB.py')
                print("Código de almacenamiento ejecutado correctamente...")

                os.system('python3 /home/vdelaluz/git/Sistemas-Distribuidos/03dataProcessing.py')
                print("Código de procesamiento ejecutado correctamente...")
            except:
                print("\n\tNo se han podido ejecutar los códigos de almacenamiento y procesamiento de datos\n")
            # Cerramos el código para que el archivo sh pueda ejecutar el siguiente código
            #print(hashtags)
            sys.exit()


        # Esta condición es por si algún hashtag sobrepasa el umbral antes de que el código termine su tiempo de ejecución.
        # Hace falta añadir un controlador, es decir, para ejecutar el código sólo una vez
        # --------------------------------------------------------------------------

        # hashtags[tag] = [1, date] manera en que son almacenados los datos
        """else:
            tmpDic = {}
            try:
                #print("ENTRE 1")

                valorSalvar = max(hashtags.values())[0]
                if int(valorSalvar) >= 2:
                    #print("ENTRE 2")

                    #claves = list(hashtags.keys())
                    #valores = list(dic.values())
                    claveSalvar = list(hashtags.keys())[list(hashtags.values()).index(valorSalvar)]
                    tmpDic[claveSalvar] = valorSalvar
                    print(hashtags, claveSalvar, valorSalvar)
                    # Corroboramos que la clave no haya sido ya añadida
                    if (claveSalvar not in saveValues):
                        #print("ENTRE 3")
                        saveValues.append(claveSalvar)
                        # Guardar los tuits
                        myJSON = json.dumps(tmpDic)
                        # Guardamos nuestros datos en un archivo json
                        now = datetime.datetime.now()
                        PATH='/home/ladiv/github/Sistemas-Distribuidos/tweets'
                        files = os.listdir(PATH)
                        controlador = (len(files))+1
                        filename = now.strftime('tweets/{0}-possible_trend-%d-%m-%Y-%H-%M.json'.format(controlador))
                        #filename = now.strftime('tweets/possible_trend-%d-%m-%Y/%H-%M-%S.json')
                        with open(filename,"w") as file:
                            file.write(myJSON)

                        file.close()
                        del(hashtag[claveSalvar])
                        print("\nTweets escritos en JSON correctamente...\n")
                        os.system('python3 /home/ladiv/github/Sistemas-Distribuidos/02storeDB.py')

                        os.system('python3 /home/ladiv/github/Sistemas-Distribuidos/03dataProcessing.py')
                        print("Save values: ", saveValues)
                        # Una vez escritos los datos en el archivo JSON
                        # Procedemos a guardarlos en la base de datos
                        # Ejecutamos el código de almacenamiento
                        #try:
                            #print("ENTRE 4")
                            #os.system('python3 /home/ladiv/github/Sistemas-Distribuidos/02storeDB.py')

                            #os.system('python3 /home/ladiv/github/Sistemas-Distribuidos/03dataProcessing.py')
                            #print(saveValues)
                        #except:
                            #print("No se han podido ejecutar los códigos de almacenamiento y procesamiento")
                    else:
                        pass
                        #print("Save values: ",saveValues)
            except:
                pass"""

        # --------------------------------------
            # ----------------------------------------------------------------
            # - Código eliminado, guardado en un archivo con los identificadores # -----
            # Por si lo vuelvo a necesitar aquí.
            # ----------------------------------------------------------------

    # Estatus de la conexión
    def on_error(self, status_code):
        print("Error de conexión", status_code)


# Creamos una clase para monitorear los tuits
stream = TweetsListener()
streamingApi = tweepy.Stream(auth=api.auth, listener=stream)

# Filtramos los datos

# Coordenanas de todo México
streamingApi.filter(locations=[-122.403460741,14.1246876254,-87.9942810535,32.5735192771])

# Obtener tuits mediante palabras clave
#tuits = streamingApi.filter(track = [])
