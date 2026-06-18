class Juego:  
    def __init__(self, jugador1, jugador2): 
        self.defensor = jugador1 #define defensor
        self.atacante = jugador2 #define atacante
        self.ronda_actual = 1 #ronda actual que se encuentran
        self.victorias_defensor = 0 #rondas ganadas por defensor
        self.victorias_atacante = 0 #rondas ganadas por el atacante
        self.dinero_inicial = 1000 #dinero que reciben los jugadores por ronda

    def iniciar_ronda(self):
        #Da dinero a los dos jugadores al iniciar ronda
        self.defensor["dinero"] = self.dinero_inicial
        self.atacante["dinero"] = self.dinero_inicial

    def registrar_victoria(self, rol):
        #Suma victoria dependiendo quien ganó
        if rol == "defensor":
            self.victorias_defensor += 1
        if rol == "atacante":
            self.victorias_atacante += 1
        self.ronda_actual += 1 #se avanza a la siguiente ronda

    def verificar_ganador(self):
        #Retorna quien ganó la partida, 
        # o None en caso de que no haya ganado nadie aún
        if self.victorias_defensor == 3:
            return "Defensor"
        if self.victorias_atacante == 3:
            return "Atacante"
        return None
    
    def __str__(self):
        return f"Ronda {self.ronda_actual} | Defensor: {self.victorias_defensor} victorias | Atacante: {self.victorias_atacante} victorias"  