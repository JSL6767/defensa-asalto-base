class Muro: #Se crea la clase, no lleva atributos 
    def __init__(self): #dentro del parentesis ya que son valores fijos
        self.nombre = "Muro"
        self.costo = 20  #Se define costo y vida fijo para todo muro
        self.vida = 150
        self.fila = None #Fila y columna son None ya que su valor se asigna
        self.columna = None #cuando se coloquen en el mapa 

    def recibir_daño(self, cantidad):
        self.vida -= cantidad  #Resta vida y retorna True si fue destruido
        return self.vida <= 0
    
    def __str__(self):
        return f"Muro | Vida: {self.vida}" #imprimir el muro