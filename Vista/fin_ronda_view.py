import tkinter as tk

COLOR_FONDO = "#1a0f1f"
COLOR_PANEL = "#3d1530"
COLOR_ACENTO = "#9b4f7f"
COLOR_TEXTO = "#e8d5e0"
COLOR_DEFENSOR = "#9b4f7f"
COLOR_ATACANTE = "#c9596f"

class FinRondaView:
    def __init__(self, root, ganador_ronda, jugador1, jugador2, victorias_defensor, victorias_atacante, callback_continuar):
        self.root = root
        self.ganador_ronda = ganador_ronda
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.victorias_defensor = victorias_defensor
        self.victorias_atacante = victorias_atacante
        self.callback_continuar = callback_continuar

        self.frame = tk.Frame(root, bg=COLOR_FONDO)
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        tk.Label(
            self.frame,
            text="Fin de Ronda",
            font=("Georgia", 20, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO
        ).pack(pady=30)

        if self.ganador_ronda == "defensor":
            nombre_ganador = self.jugador1["nombre"]
            texto = f"{nombre_ganador} defiende la base"
        else:
            nombre_ganador = self.jugador2["nombre"]
            texto = f"{nombre_ganador} destruyo la base"

        tk.Label(
            self.frame,
            text=texto,
            font=("Georgia", 14, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(pady=10)

        panel = tk.Frame(self.frame, bg=COLOR_PANEL, padx=30, pady=20)
        panel.pack(pady=20, padx=40, fill="x")

        tk.Label(
            panel,
            text="Marcador",
            font=("Georgia", 14, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_ACENTO
        ).pack(pady=5)

        fila = tk.Frame(panel, bg=COLOR_PANEL)
        fila.pack(pady=10)

        tk.Label(
            fila,
            text=f"{self.jugador1['nombre']}\nDefensor\n{self.victorias_defensor} rondas",
            font=("Georgia", 13),
            bg=COLOR_PANEL,
            fg=COLOR_DEFENSOR
        ).pack(side="left", padx=30)

        tk.Label(
            fila,
            text="contra",
            font=("Georgia", 16, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO
        ).pack(side="left", padx=20)

        tk.Label(
            fila,
            text=f"{self.jugador2['nombre']}\nAtacante\n{self.victorias_atacante} rondas",
            font=("Georgia", 13),
            bg=COLOR_PANEL,
            fg=COLOR_ATACANTE
        ).pack(side="left", padx=30)

        tk.Button(
            self.frame,
            text="Continuar",
            font=("Georgia", 13, "bold"),
            bg=COLOR_ACENTO,
            fg=COLOR_FONDO,
            command=self._continuar,
            padx=20, pady=10
        ).pack(pady=30)

    def _continuar(self):
        self.frame.destroy()
        self.callback_continuar()




        
        