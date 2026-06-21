import json
import os

RUTA_JUGADORES = "datos/jugadores.json"                #ruta del archivo donde se guardan los jugadores

def cargar_jugadores():
    if not os.path.exists(RUTA_JUGADORES):              #si el archivo no existe retorna lista vacia
        return []
    with open(RUTA_JUGADORES, "r", encoding="utf-8") as f:
        datos = json.load(f)                              #lee el contenido del json
        return datos.get("jugadores", [])                 #retorna la lista de jugadores

def guardar_jugadores(lista_jugadores):
    with open(RUTA_JUGADORES, "w", encoding="utf-8") as f:
        json.dump({"jugadores": lista_jugadores}, f, indent=4, ensure_ascii=False)   #guarda la lista completa

def registrar_jugador(nombre, contrasena):
    jugadores = cargar_jugadores()                        #carga los jugadores existentes

    for j in jugadores:
        if j["nombre"] == nombre:                          #verifica que el nombre no exista
            return False

    nuevo = {                                               #crea el jugador nuevo
        "nombre": nombre,
        "contrasena": contrasena,
        "victorias_defensor": 0,
        "victorias_atacante": 0
    }
    jugadores.append(nuevo)                                 #lo agrega a la lista
    guardar_jugadores(jugadores)                            #guarda los cambios en el json
    return True

def iniciar_sesion(nombre, contrasena):
    jugadores = cargar_jugadores()                          #carga los jugadores existentes
    for j in jugadores:
        if j["nombre"] == nombre and j["contrasena"] == contrasena:   #valida las credenciales
            return j
    return None

def actualizar_victorias(nombre, rol):
    jugadores = cargar_jugadores()                          #carga los jugadores existentes
    for j in jugadores:
        if j["nombre"] == nombre:
            if rol == "defensor":                            #suma victoria segun el rol
                j["victorias_defensor"] += 1
            elif rol == "atacante":
                j["victorias_atacante"] += 1
            break
    guardar_jugadores(jugadores)                              #guarda los cambios en el json

def obtener_top_jugadores():
    jugadores = cargar_jugadores()                            #carga todos los jugadores

    top_defensores = sorted(jugadores, key=lambda j: j["victorias_defensor"], reverse=True)[:5]   #ordena por victorias de defensor
    top_atacantes = sorted(jugadores, key=lambda j: j["victorias_atacante"], reverse=True)[:5]     #ordena por victorias de atacante

    return top_defensores, top_atacantes