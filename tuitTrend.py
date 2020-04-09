
import tweepy
import twitter
import json



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
tuits = streamingApi.filter(track = ["Morelia", "México"])
