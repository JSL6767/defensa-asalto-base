import tkinter as tk
from sistema_archivos import actualizar_victorias
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))   #permite importar desde la raiz del proyecto

COLOR_FONDO = "#1a0f1f"                                #colores de la paleta vino tinto y morado
COLOR_PANEL = "#3d1530"
COLOR_ACENTO = "#9b4f7f"
COLOR_TEXTO = "#e8d5e0"
COLOR_DEFENSOR = "#9b4f7f"
COLOR_ATACANTE = "#c9596f"

class FinPartidaView:
    def __init__(self, root, ganador_rol, jugador1, jugador2, victorias_defensor, victorias_atacante, callback_volver):
        self.root = root                                   #ventana principal
        self.ganador_rol = ganador_rol                     #rol que gano la partida
        self.jugador1 = jugador1                           #defensor
        self.jugador2 = jugador2                           #atacante
        self.victorias_defensor = victorias_defensor       #rondas ganadas por el defensor
        self.victorias_atacante = victorias_atacante       #rondas ganadas por el atacante
        self.callback_volver = callback_volver             #funcion para volver al menu

        if ganador_rol == "defensor":                       #suma la victoria al jugador que gano
            actualizar_victorias(jugador1["nombre"], "defensor")
        else:
            actualizar_victorias(jugador2["nombre"], "atacante")

        self.frame = tk.Frame(root, bg=COLOR_FONDO)         #crea el frame principal
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        if self.ganador_rol == "defensor":                   #determina nombre y color del ganador
            nombre_ganador = self.jugador1["nombre"]
            color = COLOR_DEFENSOR
        else:
            nombre_ganador = self.jugador2["nombre"]
            color = COLOR_ATACANTE

        tk.Label(
            self.frame,
            text="Fin de Partida",
            font=("Georgia", 22, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO
        ).pack(pady=30)

        tk.Label(
            self.frame,
            text=f"{nombre_ganador} gana la partida",
            font=("Georgia", 16, "bold"),
            bg=COLOR_FONDO,
            fg=color
        ).pack(pady=10)

        panel = tk.Frame(self.frame, bg=COLOR_PANEL, padx=30, pady=20)   #panel del resultado final
        panel.pack(pady=20, padx=40, fill="x")

        tk.Label(
            panel,
            text="Resultado Final",
            font=("Georgia", 14, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_ACENTO
        ).pack(pady=5)

        fila = tk.Frame(panel, bg=COLOR_PANEL)               #fila con el marcador de ambos jugadores
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
            text="Volver al Menu",
            font=("Georgia", 13, "bold"),
            bg=COLOR_ACENTO,
            fg=COLOR_FONDO,
            command=self._volver,
            padx=20, pady=10
        ).pack(pady=30)

    def _volver(self):
        self.frame.destroy()                                  #cierra esta pantalla
        self.callback_volver()                                #vuelve al menu principal

    

