class Unidad:
    def __init__(self, nombre, costo, vida, daño, velocidad):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.daño = daño
        self.velocidad = velocidad
        self.turnos_habilidad = 0
        self.congelado = False
        self.fila = None
        self.columna = None

    def recibir_daño(self, cantidad):
        self.vida -= cantidad
        return self.vida <= 0  # Retorna True si fue destruida

    def mover(self):
        if self.congelado:
            self.congelado = False  # Se descongela al siguiente turno
            return False
        self.columna -= self.velocidad  # Avanza hacia la base
        return True

    def habilidad_especial(self, objetivo):
        raise NotImplementedError("Cada unidad debe implementar su habilidad")

    def __str__(self):
        return f"{self.nombre} | Vida: {self.vida} | Daño: {self.daño} | Velocidad: {self.velocidad}"


class Soldado(Unidad):
    def __init__(self):
        super().__init__("Soldado", costo=30, vida=80, daño=15, velocidad=1)

    def habilidad_especial(self, objetivo):
        # Ataque doble cada 3 turnos
        self.turnos_habilidad += 1
        if self.turnos_habilidad >= 3:
            objetivo.recibir_daño(self.daño * 2)
            self.turnos_habilidad = 0
            return "¡Ataque doble del soldado!"
        return None


class Tanque(Unidad):
    def __init__(self):
        super().__init__("Tanque", costo=120, vida=400, daño=40, velocidad=1)

    def habilidad_especial(self, objetivo=None):
        # Escudo temporal: reduce el daño recibido a la mitad por 2 turnos
        self.turnos_habilidad += 1
        if self.turnos_habilidad >= 5:
            self.escudo = True
            self.turnos_habilidad = 0
            return "¡Escudo del tanque activado!"
        return None

    def recibir_daño(self, cantidad):
        if hasattr(self, 'escudo') and self.escudo:
            cantidad = cantidad // 2
            self.escudo = False
        return super().recibir_daño(cantidad)


class UnidadRapida(Unidad):
    def __init__(self):
        super().__init__("Unidad Rápida", costo=60, vida=50, daño=10, velocidad=3)

    def habilidad_especial(self, objetivo=None):
        # Aumento de velocidad cada 4 turnos
        self.turnos_habilidad += 1
        if self.turnos_habilidad >= 4:
            self.velocidad = 5
            self.turnos_habilidad = 0
            return "¡Velocidad aumentada!"
        return None
    
#mensaje de prueba
