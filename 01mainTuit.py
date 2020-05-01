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
# Lista para guardar los hashtags
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
        # Hacemos un recorrido por los hashtags y comparamos con nuestro diccionario de hashtags
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
                    hashtags[tag] = 1
                    date = data["publication_date"] # obtener la fecha
                    #print(date)
                    date = date.split(" ")
                    hour = date[1]
                    today = date[0]
                    time_vector.append(hour)
                    tag_vector.append(tag)
        
        
    
        
                
        elapsed_time = time.time() - start_time # Obtenemos el tiempo transcurrido
        elapsed_time_seg = int(elapsed_time) # Obtenemos los segundos
        
        if elapsed_time_seg == 2800:
            # Para no estar generando gráficas que no nos aporten nuevo conocimiento, 
            # nos limitaremos a generar graficas con los hashtags que logren pasar
            # o igualar el umbral para considerar "posible tendencía"
        
            arr_de_etiquetas = [] # Arrreglo de etiquetas para graficar nombramiento de puntos
            arr_de_valores = [] # arreglo de valores para graficar
            for clave in hashtags.keys():
                
                if hashtags[clave] >= 50: 
                    arr_de_etiquetas.append(clave)
                    arr_de_valores.append(hashtags[clave])
                #else:
                    #print(max(hashtags.values()))
                    #sys.exit()
            arr_temp = [int(i) for i in range(len(arr_de_etiquetas))] # arreglo temporal para el eje x 
            
            # Graficar
            fig, ax = plt.subplots()
            now = datetime.datetime.now()
            actual_date = now.strftime('Day :%d, Month: %m, Year: %Y, Hour: %H, Minutes: %M, Seconds: %S')
            #ax.set_title(datetime.date.today())
            ax.set_title(actual_date)
            ax.set_xlabel("Tags")
            ax.set_ylabel("Number of tweets")
            font = {'family' : 'normal', 'weight' : 'normal', 'size'   : 8}
         
            ax.plot(arr_temp, arr_de_valores, "-or")
            
            #ax.set_xticklabels(arr_de_etiquetas, font, rotation=90)
            ax.grid()
            
            # Establecer el tamaño de los ejes
            plt.ylim(0, max(arr_de_valores)+5)
            plt.yscale("linear")
            
            # Etiquetar los puntos
            ids = arr_de_etiquetas
            for i, txt in enumerate(ids): 
                plt.annotate(str(txt), (arr_temp[i], arr_de_valores[i]))
            
            
            # Guardamos la gráfica 
            today = datetime.datetime.now()
            #día-mes-año - horas-minutos-segundos
            actual_day = now.strftime('%d-%m-%Y-%H-%M-%S.png')
            plt.savefig(actual_day, bbox_inches='tight')
            plt.show()
            
           
            
        
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
