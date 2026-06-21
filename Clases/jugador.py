class Jugador:
    def __init__(self, nombre, contrasena):
        self.nombre = nombre                            #guarda el nombre del jugador
        self.contrasena = contrasena                    #guarda la contrasena del jugador
        self.victorias_defensor = 0                     #contador de victorias como defensor
        self.victorias_atacante = 0                      #contador de victorias como atacante
        self.dinero = 0                                  #dinero actual del jugador
        self.faccion = None                              #faccion elegida, vacia al inicio

    def agregar_victoria_defensor(self):
        self.victorias_defensor += 1                     #suma una victoria como defensor

    def agregar_victoria_atacante(self):
        self.victorias_atacante += 1                     #suma una victoria como atacante

    def establecer_dinero(self, cantidad):
        self.dinero = cantidad                           #fija el dinero a una cantidad exacta

    def gastar_dinero(self, cantidad):
        if cantidad <= self.dinero:                      #verifica que alcance el dinero
            self.dinero -= cantidad                       #resta el dinero gastado
            return True
        return False                                      #no tiene suficiente dinero

    def ganar_dinero(self, cantidad):
        self.dinero += cantidad                           #suma dinero ganado

    def a_dict(self):
        return {                                          #convierte el jugador a diccionario
            "nombre": self.nombre,                        #para guardarlo en el json
            "contrasena": self.contrasena,
            "victorias_defensor": self.victorias_defensor,
            "victorias_atacante": self.victorias_atacante
        }