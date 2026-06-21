class Unidad:
    def __init__(self, nombre, costo, vida, daño, velocidad):
        self.nombre = nombre                              #nombre de la unidad
        self.costo = costo                                 #precio para comprarla
        self.vida = vida                                   #vida actual de la unidad
        self.daño = daño                                   #daño que hace por ataque
        self.velocidad = velocidad                          #casillas que avanza por turno
        self.turnos_habilidad = 0                           #contador sin uso actualmente
        self.congelado = False                              #si esta congelada por una torre
        self.fila = None                                    #posicion en el mapa, vacia al inicio
        self.columna = None

    def recibir_daño(self, cantidad):
        self.vida -= cantidad                               #resta vida al recibir daño
        return self.vida <= 0                                #retorna true si fue destruida

    def mover(self):
        if self.congelado:                                   #si esta congelada no se mueve
            self.congelado = False                            #se descongela al siguiente turno
            return False
        self.columna -= self.velocidad                        #avanza hacia la base
        return True

    def habilidad_especial(self, objetivo):
        raise NotImplementedError("Cada unidad debe implementar su habilidad")   #cada subclase la define

    def __str__(self):
        return f"{self.nombre} | Vida: {self.vida} | Daño: {self.daño} | Velocidad: {self.velocidad}"   #texto para mostrar la unidad


class Soldado(Unidad):
    def __init__(self):
        super().__init__("Soldado", costo=30, vida=80, daño=15, velocidad=1)   #valores fijos del soldado

    def habilidad_especial(self, objetivo):
        if objetivo:                                          #si hay un objetivo valido
            objetivo.recibir_daño(self.daño * 2)               #le hace el doble de daño
            return "¡Ataque doble del soldado!"
        return None


class Tanque(Unidad):
    def __init__(self):
        super().__init__("Tanque", costo=120, vida=400, daño=40, velocidad=1)   #valores fijos del tanque

    def habilidad_especial(self, objetivo=None):
        self.escudo = True                                    #activa el escudo temporal
        return "¡Escudo del tanque activado!"

    def recibir_daño(self, cantidad):
        if hasattr(self, 'escudo') and self.escudo:             #si tiene escudo activo
            cantidad = cantidad // 2                              #reduce el daño a la mitad
            self.escudo = False                                   #consume el escudo
        return super().recibir_daño(cantidad)                     #aplica el daño normal


class UnidadRapida(Unidad):
    def __init__(self):
        super().__init__("Unidad Rápida", costo=60, vida=50, daño=10, velocidad=3)   #valores fijos de la unidad rapida

    def habilidad_especial(self, objetivo=None):
        self.velocidad = 5                                       #aumenta la velocidad de avance
        return "¡Velocidad aumentada!"
