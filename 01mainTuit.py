import tweepy
import twitter
import json
import requests
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys
import time

# Tiempo para el control de la recepción de tuits (esta en segundos)
start_time = time.time() 

# Diccionario para controlar el número de hashtags
hashtags = {}
# Lista para guardar el tiempo en el que el tuit fue publicado
time_vector = []
# Lista para obtener el total de tuits
tag_vector = []

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
        if len(hasht) != 0:
            print(status.text)
            for dicci in hasht: 
                tag = dicci["text"]
                tag = tag.lower()
                #print(tag)
                if (tag in hashtags.keys()) == True:
                    hashtags[tag] += 1
                else: 
                    #print("entre")
                    hashtags[tag] = 0
                    date = data["publication_date"] # obtener la fecha
                    print(date)
                    date = date.split(" ")
                    hour = date[1]
                    today = date[0]
                    time_vector.append(hour)
        
        
        elapsed_time = time.time() - start_time # Obtenemos el tiempo transcurrido
        elapsed_time_seg = int(elapsed_time) # Obtenemos los segundos
        
        if elapsed_time_seg == 120:
            time_tag = list(hashtags.values())
            #print(time_vector, time_tag)
            # Graficar
            fig, ax = plt.subplots()
            ax.plot(time_vector, time_tag, "or")
            ax.set(xlabel='time(seg)', ylabel='number of tweets', title=datetime.date.today())
            ax.grid()
            plt.ylim(0, 10)
            plt.yscale("linear")
            #fig.savefig("/trends.png")
            plt.show()
            print(hashtags)
        
                
            
        
    # Estatus de la conexión
    def on_error(self, status_code):
        print("Error de conexión", status_code)



  
# Creamos una clase para monitorear los tuits
stream = TweetsListener()
streamingApi = tweepy.Stream(auth=api.auth, listener=stream)

# Filtramos los datos

# Coordenanas de toda latinoamerica
streamingApi.filter(locations=[-122.403460741,14.1246876254,-87.9942810535,32.5735192771]) 

# Obtener tuits mediante palabras clave
#tuits = streamingApi.filter(track = ["ladiv", "Ladiv", "vidale", "Vidale"])
