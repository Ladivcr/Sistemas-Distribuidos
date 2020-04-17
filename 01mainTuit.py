import tweepy
import twitter
import json
import requests
import json
import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys



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

    # Recibimos los tuits
    def on_status(self, status):
        print("\nTweets: {0}\nHashtags: {1}\nId user: {2}\nName user: {3}\
              \n@ User: {4}\nProfile description: {5}\nLocation: {6}\
              \n# Followers: {7}\nTotal profile tweets: {8}\nPublication date: {9}"
              .format(status.text, status.entities["hashtags"], status.user.id_str, status.user.name, status.user.screen_name, status.user.description, 
                      status.coordinates, status.user.followers_count, status.user.statuses_count, status.created_at))
              
        publication_date = str(status.created_at)
        #print(type(publication_date))
        #mytime = datetime.datetime.strptime(publication_date, '%Y-%m-%d %H:%M:%S')
        #print(type(mytime))
        response = {"hashtags":status.entities["hashtags"], "coordinates":status.coordinates,"publication_date":publication_date}
        
        # Convertimos los atributos con los que vamos a trabajar en un dato del tipo JSON
        data = json.dumps(response)
        
        # Cargamos los datos ahora como un tipo de dato JSON
        data = json.loads(data)
        tags = {}
        time_vector = []
        tag_vector = []
        for item in data.items():
            #print(item)
            if item[0] == "hashtags":
                for tag in item[1]:
                    if (tag in tags) == True: 
                        tags[tag] += 1
                    else: 
                        tags[tag] = 0
                    
            if item[0] == "publication_date":
                #print(type(item[1]))
                mytime = datetime.datetime.strptime(item[1], '%Y-%m-%d %H:%M:%S')
                #print(type(mytime))
                try:
                    time_vector.append(mytime)
                    tag_vector.append(max(tags.values()))
                except ValueError:
                    time_vector.append(mytime)
                    tag_vector.append(0)
        # Graficar
        fig, ax = plt.subplots()
        ax.plot(time_vector, tag_vector)
        ax.set(xlabel='time', ylabel='trends', title='trends')
        ax.grid()
        #plt.ylim(1e-9, 1e-2)
        #plt.yscale("log")
        fig.savefig("/trends.png")
        plt.show()

                
                
            
        
        
    # Estatus de la conexión
    def on_error(self, status_code):
        print("Error de conexión", status_code)



  
# Creamos una clase para monitorear los tuits
stream = TweetsListener()
streamingApi = tweepy.Stream(auth=api.auth, listener=stream)

# Filtramos los datos

# Coordenanas de toda latinoamerica
#streamingApi.filter(locations=[-120.5752312537,11.5864357452,-85.4274408173,34.9875682623]) 

# Obtener tuits mediante palabras clave
tuits = streamingApi.filter(track = ["México"])
