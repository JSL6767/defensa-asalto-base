class Torre:
    def __init__(self, nombre, costo, vida, daño, alcance):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.daño = daño
        self.alcance = alcance
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
        # Disparo doble (activado manualmente, sin contador interno)
        if objetivo:
            objetivo.recibir_daño(self.daño * 2)
            return "¡Disparo doble activado!"
        return None


class TorrePesada(Torre):
    def __init__(self):
        super().__init__("Torre Pesada", costo=150, vida=300, daño=60, alcance=2)

    def habilidad_especial(self, objetivos):
        # Daño en área (activado manualmente, sin contador interno)
        if objetivos:
            for objetivo in objetivos:
                objetivo.recibir_daño(self.daño // 2)
            return "¡Daño en área activado!"
        return None


class TorreMagica(Torre):
    def __init__(self):
        super().__init__("Torre Mágica", costo=100, vida=80, daño=10, alcance=5)

    def habilidad_especial(self, objetivo):
        # Congelar (activado manualmente, sin contador interno)
        if objetivo:
            objetivo.congelado = True
            return "¡Unidad congelada!"
        return None