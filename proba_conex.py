from spotify_manager import obtener_top_tracks

canciones = obtener_top_tracks()
for nombre, artista, _ in canciones:
    print(f"{nombre} - {artista}")

