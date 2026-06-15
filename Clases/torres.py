class Torre:
    def __init__(self, nombre, costo, vida, daño, alcance):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.daño = daño
        self.alcance = alcance
        self.turnos_habilidad = 0  # Contador para activar habilidad
        self.fila = None
        self.columna = None

    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        return self.vida <= 0  # Retorna True si fue destruida

    def habilidad_especial(self, objetivo):
        raise NotImplementedError("Cada torre debe implementar su habilidad")

    def __str__(self):
        return f"{self.nombre} | Vida: {self.vida} | Daño: {self.daño} | Alcance: {self.alcance}"


class TorreBasica(Torre):
    def __init__(self):
        super().__init__("Torre Básica", costo=50, vida=100, daño=20, alcance=3)

    def habilidad_especial(self, objetivo):
        # Disparo doble: ataca dos veces cada 3 turnos
        self.turnos_habilidad += 1
        if self.turnos_habilidad >= 3:
            objetivo.recibir_daño(self.daño * 2)
            self.turnos_habilidad = 0
            return "¡Disparo doble activado!"
        return None


class TorrePesada(Torre):
    def __init__(self):
        super().__init__("Torre Pesada", costo=150, vida=300, daño=60, alcance=2)

    def habilidad_especial(self, objetivos):
        # Daño en área: daña a todas las unidades cercanas cada 4 turnos
        self.turnos_habilidad += 1
        if self.turnos_habilidad >= 4:
            for objetivo in objetivos:
                objetivo.recibir_daño(self.daño // 2)
            self.turnos_habilidad = 0
            return "¡Daño en área activado!"
        return None


class TorreMagica(Torre):
    def __init__(self):
        super().__init__("Torre Mágica", costo=100, vida=80, daño=10, alcance=5)

    def habilidad_especial(self, objetivo):
        # Congelar: la unidad pierde su turno cada 3 turnos
        self.turnos_habilidad += 1
        if self.turnos_habilidad >= 3:
            objetivo.congelado = True
            self.turnos_habilidad = 0
            return "¡Unidad congelada!"
        return None