import tkinter as tk

class FinRondaView:
    def __init__(self, root, ganador_ronda, jugador1, jugador2, victorias_defensor, victorias_atacante, callback_continuar):
        self.root = root
        self.ganador_ronda = ganador_ronda #defensor o atacante
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.victorias_defensor = victorias_defensor 
        self.victorias_atacante = victorias_atacante
        self.callback_continuar = callback_continuar  #función para continuar al siguiente

        self.frame = tk.Frame(root, bg="#1a1a2e")
        self.frame.pack(fill="both", expand= True)

        self._construir_ui()

    def _construir_ui(self):
        #título
        tk.Label(
            self.frame,
            text="⚔ Fin de Ronda ⚔",
            font=("Arial", 20, "bold"),
            bg="#1a1a2e",
            fg="#c9a84c"
        ).pack(pady=30)

        #quién ganó la ronda
        if self.ganador_ronda == "defensor":
            nombre_ganador = self.jugador1["nombre"]
            color_ganador = "#3498db"
            texto = f"🛡 {nombre_ganador} defiende la base!"
        else:
            nombre_ganador = self.jugador2["nombre"]
            color_ganador = "#e74c3c"
            texto = f"⚔ {nombre_ganador} destruyó la base!"

        tk.Label(
            self.frame,
            text=texto,
            font=("Arial", 14, "bold"),
            bg="#1a1a2e",
            fg=color_ganador
        ).pack(pady=10)

        #marcador de rondas
        panel = tk.Frame(self.frame, bg="#16213e", padx=30, pady=20)
        panel.pack(pady=20, padx=40, fill="x")

        tk.Label(
            panel,
            text="Marcador",
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="#c9a84c"
        ).pack(pady=5)

        #fila con nombres y victorias
        fila = tk.Frame(panel, bg="#16213e")
        fila.pack(pady=10)

        #defensor
        tk.Label(
            fila,
            text=f"{self.jugador1['nombre']}\n🛡 Defensor\n{self.victorias_defensor} rondas",
            font=("Arial", 13),
            bg="#16213e",
            fg="#3498db"
        ).pack(side="left", padx=30)

        tk.Label(
            fila,
            text="VS",
            font=("Arial", 16, "bold"),
            bg="#16213e",
            fg="white"
        ).pack(side="left", padx=20)

        #atacante
        tk.Label(
            fila,
            text=f"{self.jugador2['nombre']}\n⚔ Atacante\n{self.victorias_atacante} rondas",
            font=("Arial", 13),
            bg="#16213e",
            fg="#e74c3c"
        ).pack(side="left", padx=30)

        #botón para continuar
        tk.Button(
            self.frame,
            text="Continuar",
            font=("Arial", 13, "bold"),
            bg="#c9a84c",
            fg="#1a1a2e",
            command=self._continuar,
            padx=20, pady=10
        ).pack(pady=30)

    def _continuar(self):
        #cierra la ventana para continuar
        self.frame.destroy()
        self.callback_continuar()




        
        