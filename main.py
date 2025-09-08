import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Entry
import os 
from spotify_manager import (
    obtener_top_tracks,
    obtener_top_tracks_anual,
    crear_playlist,
    obtener_nombre_mes_para_playlist,
    obtener_anio_actual,
    guardar_credenciales_env
)

if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        pass 

VERDE_SPOTIFY = "#1DB954"
BLANCO = "#FFFFFF"
TEXTO = "#FFFFFF"


ventana = tk.Tk()
ventana.title("🎧 Generador de Playlists Spotify")
ventana.geometry("520x480") 
ventana.configure(bg=VERDE_SPOTIFY)


link_var = tk.StringVar()

def abrir_ventana_credenciales():
    popup = Toplevel(ventana)
    popup.title("Configurar Credenciales de Spotify")
    popup.geometry("400x200")
    popup.configure(bg="#2c2c2c")
    popup.grab_set() 

    Label(popup, text="SPOTIPY_CLIENT_ID:", fg=TEXTO, bg="#2c2c2c").pack(pady=(10, 0))
    client_id_entry = Entry(popup, width=50)
    client_id_entry.pack()

    Label(popup, text="SPOTIPY_CLIENT_SECRET:", fg=TEXTO, bg="#2c2c2c").pack(pady=(10, 0))
    client_secret_entry = Entry(popup, width=50)
    client_secret_entry.pack()

    Label(popup, text="SPOTIPY_REDIRECT_URI:", fg=TEXTO, bg="#2c2c2c").pack(pady=(10, 0))
    redirect_uri_entry = Entry(popup, width=50)
    redirect_uri_entry.pack()
    
    def guardar_y_cerrar():
        client_id = client_id_entry.get()
        client_secret = client_secret_entry.get()
        redirect_uri = redirect_uri_entry.get()

        if not client_id or not client_secret or not redirect_uri:
            messagebox.showwarning("Campos vacíos", "Por favor, ingresa ambos valores.", parent=popup)
            return
            
        guardar_credenciales_env(client_id, client_secret, redirect_uri)
        messagebox.showinfo("Éxito", "Credenciales guardadas. La aplicación usará estas credenciales la próxima vez que crees una playlist.", parent=popup)
        popup.destroy()

    btn_guardar = tk.Button(popup, text="Guardar", command=guardar_y_cerrar)
    btn_guardar.pack(pady=20)


def generar_top_playlist():
    try:
        canciones = obtener_top_tracks()
        if not canciones:
            messagebox.showerror("Error", "No se pudieron obtener tus canciones más escuchadas.")
            return
        ids = [track_id for _, _, track_id in canciones]
        nombre = f"Top de {obtener_nombre_mes_para_playlist()}"
        url = crear_playlist(nombre, ids)
        link_var.set(url)
        etiqueta_resultado.config(text="🎧 Playlist Top Mensual creada:", fg=TEXTO)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a Spotify. Revisa tus credenciales.\n\nError: {e}")

def generar_playlist_anual():
    try:
        canciones = obtener_top_tracks_anual()
        if not canciones:
            messagebox.showerror("Error", "No se pudieron obtener tus canciones más escuchadas del año.")
            return
        ids = [track_id for _, _, track_id in canciones]
        nombre = f"Top {len(ids)} de {obtener_anio_actual()}"
        url = crear_playlist(nombre, ids)
        link_var.set(url)
        etiqueta_resultado.config(text="📅 Playlist Top Anual creada:", fg=TEXTO)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a Spotify. Revisa tus credenciales.\n\nError: {e}")


etiqueta = tk.Label(ventana, text="🎧 Generador de playlists", font=("Segoe UI", 14, "bold"), bg=VERDE_SPOTIFY, fg=TEXTO)
etiqueta.pack(pady=20)


def crear_boton(texto, comando, width=40):
    return tk.Button(
        ventana, text=texto, command=comando,
        font=("Segoe UI", 11, "bold"),
        bg=BLANCO, fg=VERDE_SPOTIFY,
        activebackground="#f0f0f0", activeforeground=VERDE_SPOTIFY,
        relief="flat", width=width, height=2
    )

btn_top = crear_boton("🎧 Crear playlist de lo más escuchado del mes", generar_top_playlist)
btn_top.pack(pady=10)

btn_anual = crear_boton("📅 Crear playlist de lo más escuchado del año", generar_playlist_anual)
btn_anual.pack(pady=10)

btn_config = crear_boton("⚙️ Configurar Credenciales", abrir_ventana_credenciales, width=25)
btn_config.pack(pady=(0, 10))


etiqueta_resultado = tk.Label(ventana, text="", font=("Segoe UI", 10, "bold"), bg=VERDE_SPOTIFY, fg=TEXTO)
etiqueta_resultado.pack(pady=5)

cuadro_link = tk.Entry(ventana, textvariable=link_var, width=60, font=("Segoe UI", 10), justify="center")
cuadro_link.pack(pady=5)

btn_copiar = tk.Button(
    ventana, text="📋 Copiar enlace",
    command=lambda: (ventana.clipboard_clear(), ventana.clipboard_append(link_var.get())),
    font=("Segoe UI", 10),
    bg=BLANCO, fg=VERDE_SPOTIFY,
    relief="flat", width=20
)

btn_copiar.pack(pady=10)

ventana.mainloop()



