from dotenv import load_dotenv
import os
import sys
import base64
from requests import post, get
import json

load_dotenv()
#obtengo las variables de entorno
app_id = os.getenv("CLIENT_ID")
app_secret = os.getenv("CLIENT_SECRET")


#Función que recibira el token de autorización
#Como  lo pide la documentación de Spotify
def get_token():
    #Concateno id & secret , lo paso a base 64   
    try: 
        credencials_encoded = base64.b64encode((app_id + ":" + app_secret).encode("ascii")).decode("ascii")
    
        url= "https://accounts.spotify.com/api/token"
        headers= {
            "Authorization": "Basic " + credencials_encoded,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data= {'grant_type': 'client_credentials'}
        result= post(url, headers=headers, data=data)
        #convierto la respuesta del json a un diccionario
        json_result= json.loads(result.content)   
        token= json_result["access_token"]    
        return token
    except:
        print("Something wrog with your TOKEN")

def get_auth2_header(token):
    return {"Authorization": "Bearer " + token}

#buscamos el nombre del artista con filtro de resultado por artista
def search_for_artist(token):
    try:
        artist= input("Type your favourite artist: ")    
        #la query de la url indica que la busqueda sera por artista y con un solo resultado (type: artist / limit:1)
        url=f"https://api.spotify.com/v1/search?q={artist}&type=artist&limit=1"
        headers= get_auth2_header(token)
        result= get(url, headers=headers)
        json_result= json.loads(result.content)["artists"]["items"]
        if len(json_result) == 0:
            print("No artist availables with this name... ")
            search_for_artist(token)
        #retorna el id del artista
        return json_result[0]["id"]
    except:
        print('Something wrong searching your artist, try again')
        search_for_artist(token)

#busqueda el top 10 por artista
def get_songs_by_artist(token):
    try:
        artist_id= search_for_artist(token)
        url= f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
        headers=get_auth2_header(token)
        result= get(url, headers=headers)    
        json_result= json.loads(result.content)["tracks"]
        return json_result
    except:
        print('Something wrong with top ten, try again')
        

token= get_token()
songs_results= get_songs_by_artist(token)

#Mostramos la lista del 1 al 10
def show_top_ten (songs_results):
    list_of_songs={}
    for i, song in enumerate(songs_results):
        name= song['name']
        number= i+1
        popularity= song['popularity']
        duration= song['duration_ms']
        print(f'{number}. {name} / Top : {popularity}')    
        #agregamos a lista al diccionario "list_of_songs"
        list_of_songs[f'{number}'] = {'name': f'{name}', 'popularity': f'{popularity}' , 'duration': f'{duration}'  }
    return list_of_songs        
 
top_ten= show_top_ten(songs_results)
my_list={}    

#Funcion para agregar a tu lista las canciones    
def add_song_list(top_ten):      
    res= input("Do you want add a new song in your list : Y / N  :") 
    if res.upper() == 'N' and len(my_list)>=2:
        print("List complete")       
        return my_list  
    if res.upper() == 'N' and len(my_list)<2:
        print("You need to add more music in your playlist")
        add_song_list(top_ten)             
    if res.upper() == 'Y':
        number_of_song= input("Enter the song NUMBER that you want add in your list: ")
        try:
            song_int= int(number_of_song)            
            my_new_song= top_ten[f'{song_int}']
            list_number= len(my_list) + 1
            #agregamos la cancion al diccionario "my_list"
            my_list[f'{list_number}']=my_new_song            
            print("New song added:", my_list[f'{list_number}']['name'])            
            add_song_list(top_ten)
        except:
            print("Enter no valid, try again")
            add_song_list(top_ten)  
    elif res.upper() != 'N' and res.upper() != 'Y':
        print("Enter no valid")
        add_song_list(top_ten)    
        
      
add_song_list(top_ten)
songs_time_list=[]

#Lista de los segundos por cancion
def total_time_of_list(my_list, songs_time_list): 
    for i in my_list:
        name= my_list[f'{i}']['name'] 
        number= i
        popularity= my_list[f'{i}']['popularity']  
        print(f'{number}. {name} / Top : {popularity}')           
        duration= my_list[f'{i}']['duration']          
        songs_time_list.append(int(f'{duration}')) 
    return songs_time_list 
   
#imprime la lista y el total de tiempo de la lista  
print(' Your playlist is : ')
total_time=  total_time_of_list(my_list, songs_time_list)
#suma el tiempo de la playlist y la imprime
print(f'Your playlist duration is:  {sum(total_time)} ')  

        
        
    
    

    


    


