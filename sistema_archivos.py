import json
import os

RUTA_JUGADORES = "datos/jugadores.json"
# Lee el archivo JSON y retorna la lista de jugadores
def cargar_jugadores():
   
    if not os.path.exists(RUTA_JUGADORES):
        return []
    with open(RUTA_JUGADORES, "r", encoding="utf-8") as f:
        datos = json.load(f)
        return datos.get("jugadores", [])
#Guarda la lista completa de jugadores en el archivo JSON.
def guardar_jugadores(lista_jugadores):
    
    with open(RUTA_JUGADORES, "w", encoding="utf-8") as f:
        json.dump({"jugadores": lista_jugadores}, f, indent=4, ensure_ascii=False)

#Registra un jugador nuevo. Retorna True si fue exitoso, False si ya existe.
def registrar_jugador(nombre, contrasena):
   
    jugadores = cargar_jugadores()
    
    # Verificar si el nombre ya existe
    for j in jugadores:
        if j["nombre"] == nombre:
            return False  # Ya existe
    
    nuevo = {
        "nombre": nombre,
        "contrasena": contrasena,
        "victorias_defensor": 0,
        "victorias_atacante": 0
    }
    jugadores.append(nuevo)
    guardar_jugadores(jugadores)
    return True
#Verifica credenciales. Retorna el dict del jugador si es correcto, None si no.
def iniciar_sesion(nombre, contrasena):
    
    jugadores = cargar_jugadores()
    for j in jugadores:
        if j["nombre"] == nombre and j["contrasena"] == contrasena:
            return j
    return None
#Suma una victoria al jugador según su rol ('defensor' o 'atacante').
def actualizar_victorias(nombre, rol):
    #Suma una victoria al jugador según su rol ('defensor' o 'atacante').
    jugadores = cargar_jugadores()
    for j in jugadores:
        if j["nombre"] == nombre:
            if rol == "defensor":
                j["victorias_defensor"] += 1
            elif rol == "atacante":
                j["victorias_atacante"] += 1
            break
    guardar_jugadores(jugadores)
#Retorna los top 5 defensores y top 5 atacantes.
def obtener_top_jugadores():
    
    jugadores = cargar_jugadores()
    
    top_defensores = sorted(jugadores, key=lambda j: j["victorias_defensor"], reverse=True)[:5]
    top_atacantes = sorted(jugadores, key=lambda j: j["victorias_atacante"], reverse=True)[:5]
    
    return top_defensores, top_atacantes