class Jugador:
    def __init__(self, nombre, contrasena):
        self.nombre = nombre
        self.contrasena = contrasena
        self.victorias_defensor = 0
        self.victorias_atacante = 0
        self.dinero = 0
        self.faccion = None

    def agregar_victoria_defensor(self):
        self.victorias_defensor += 1

    def agregar_victoria_atacante(self):
        self.victorias_atacante += 1

    def establecer_dinero(self, cantidad):
        self.dinero = cantidad

    def gastar_dinero(self, cantidad):
        if cantidad <= self.dinero:
            self.dinero -= cantidad
            return True
        return False  # No tiene suficiente dinero

    def ganar_dinero(self, cantidad):
        self.dinero += cantidad

    def a_dict(self):
        # Para guardar en JSON
        return {
            "nombre": self.nombre,
            "contrasena": self.contrasena,
            "victorias_defensor": self.victorias_defensor,
            "victorias_atacante": self.victorias_atacante
        }