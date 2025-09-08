import os
import calendar
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = None

def get_sp_client():
    global sp
    if sp is None:
        load_dotenv(find_dotenv())
        client_id = os.getenv("SPOTIPY_CLIENT_ID")
        client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            raise Exception("Credenciales no configuradas. Por favor, configúralas primero.")
            
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope="user-top-read user-library-read playlist-modify-public"
        ))
    return sp

def guardar_credenciales_env(client_id, client_secret, redirect_uri ):
    global sp
    with open(".env", "w") as f:
        f.write(f"SPOTIPY_CLIENT_ID={client_id}\n")
        f.write(f"SPOTIPY_CLIENT_SECRET={client_secret}\n")
        f.write(f"SPOTIPY_REDIRECT_URI={redirect_uri}\n")
    sp = None

def obtener_top_tracks(limit=20):
    client = get_sp_client() 
    top_tracks = client.current_user_top_tracks(time_range='short_term', limit=limit)
    return [(track['name'], track['artists'][0]['name'], track['id']) for track in top_tracks['items']]

def obtener_top_tracks_anual(limit=50):
    client = get_sp_client() 
    top_tracks = client.current_user_top_tracks(time_range='long_term', limit=limit)
    return [(track['name'], track['artists'][0]['name'], track['id']) for track in top_tracks['items']]

def crear_playlist(nombre, track_ids):
    client = get_sp_client() 
    user_id = client.current_user()['id']
    playlist = client.user_playlist_create(user=user_id, name=nombre, public=True)
    if track_ids:
        client.playlist_add_items(playlist_id=playlist['id'], items=track_ids)
    return playlist['external_urls']['spotify']

def obtener_nombre_mes_para_playlist():
    hoy = datetime.today()
    if hoy.day < 20:
        mes = hoy.month - 1 or 12
        anio = hoy.year if hoy.month > 1 else hoy.year - 1
    else:
        mes = hoy.month
        anio = hoy.year
    nombre_mes = calendar.month_name[mes]
    nombre_mes_es = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }
    return f"{nombre_mes_es[nombre_mes]} {anio}"

def obtener_anio_actual():
    return datetime.today().year

