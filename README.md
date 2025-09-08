SpotifyApp
Aplicación de escritorio para gestionar playlists de Spotify.  
Desarrollada en **Python 3.13** con 
[Spotipy](https://spotipy.readthedocs.io/), 
[Requests-OAuthlib](https://requests-oauthlib.readthedocs.io/),
[Python-Dotenv](https://pypi.org/project/python-dotenv/).  

Permite autenticarse con Spotify, crear y gestionar playlists, y guardar credenciales de forma segura en un archivo `.env`.

Características
- Autenticación con **Spotify OAuth 2.0**.
- Generación automática del archivo `.env` si no existe.
- Creación de playlists y almacenamiento de credenciales.
- Empaquetado con **PyInstaller** → funciona sin instalar Python.

Instalación y uso

1. Requisitos
- Cuenta de desarrollador en [Spotify for Developers](https://developer.spotify.com/dashboard/).
- Un **Client ID**, **Client Secret** y **Redirect URI** configurados.

2. Ejecutable
Descarga el archivo compilado en la carpeta dist/SpotifyApp.exe

