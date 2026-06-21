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

class FinDineroView:
    def __init__(self, root, jugador1, jugador2, callback_volver):
        self.root = root                                  #ventana principal
        self.jugador1 = jugador1                           #defensor, gana la partida
        self.jugador2 = jugador2                           #atacante, se quedo sin dinero
        self.callback_volver = callback_volver             #funcion para volver al menu

        actualizar_victorias(jugador1["nombre"], "defensor")   #suma la victoria automatica al defensor

        self.frame = tk.Frame(root, bg=COLOR_FONDO)        #crea el frame principal
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        tk.Label(
            self.frame,
            text="Fin de Partida",
            font=("Georgia", 22, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO
        ).pack(pady=30)

        tk.Label(
            self.frame,
            text=f"{self.jugador1['nombre']} gana la partida",     #anuncia el ganador
            font=("Georgia", 16, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_DEFENSOR
        ).pack(pady=10)

        tk.Label(
            self.frame,
            text=f"{self.jugador2['nombre']} se quedo sin dinero suficiente para continuar",   #explica el motivo
            font=("Georgia", 12),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO,
            wraplength=400
        ).pack(pady=10)

        panel = tk.Frame(self.frame, bg=COLOR_PANEL, padx=30, pady=20)   #panel del resultado
        panel.pack(pady=20, padx=40, fill="x")

        tk.Label(
            panel,
            text="Resultado",
            font=("Georgia", 14, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_ACENTO
        ).pack(pady=5)

        fila = tk.Frame(panel, bg=COLOR_PANEL)              #fila con ambos jugadores
        fila.pack(pady=10)

        tk.Label(
            fila,
            text=f"{self.jugador1['nombre']}\nDefensor\nGanador",
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
            text=f"{self.jugador2['nombre']}\nAtacante\nSin fondos",
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