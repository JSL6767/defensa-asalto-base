class Torre:
    def __init__(self, nombre, costo, vida, daño, alcance):
        self.nombre = nombre                             #nombre de la torre
        self.costo = costo                                #precio para comprarla
        self.vida = vida                                  #vida actual de la torre
        self.daño = daño                                  #daño que hace por ataque
        self.alcance = alcance                            #distancia maxima de ataque
        self.fila = None                                  #posicion en el mapa, vacia al inicio
        self.columna = None

    def recibir_daño(self, cantidad):
        self.vida -= cantidad                             #resta vida al recibir daño
        return self.vida <= 0                             #retorna true si fue destruida

    def habilidad_especial(self, objetivo):
        raise NotImplementedError("Cada torre debe implementar su habilidad")   #cada subclase la define

    def __str__(self):
        return f"{self.nombre} | Vida: {self.vida} | Daño: {self.daño} | Alcance: {self.alcance}"   #texto para mostrar la torre


class TorreBasica(Torre):
    def __init__(self):
        super().__init__("Torre Básica", costo=50, vida=100, daño=20, alcance=3)   #valores fijos de la torre basica

    def habilidad_especial(self, objetivo):
        if objetivo:                                      #si hay un objetivo valido
            objetivo.recibir_daño(self.daño * 2)           #le hace el doble de daño
            return "¡Disparo doble activado!"
        return None


class TorrePesada(Torre):
    def __init__(self):
        super().__init__("Torre Pesada", costo=150, vida=300, daño=60, alcance=2)   #valores fijos de la torre pesada

    def habilidad_especial(self, objetivos):
        if objetivos:                                      #si hay unidades en el mapa
            for objetivo in objetivos:                      #recorre todas las unidades
                objetivo.recibir_daño(self.daño // 2)        #les hace daño en area
            return "¡Daño en área activado!"
        return None


class TorreMagica(Torre):
    def __init__(self):
        super().__init__("Torre Mágica", costo=100, vida=80, daño=10, alcance=5)   #valores fijos de la torre magica

    def habilidad_especial(self, objetivo):
        if objetivo:                                       #si hay un objetivo valido
            objetivo.congelado = True                       #lo deja congelado un turno
            return "¡Unidad congelada!"
        return None