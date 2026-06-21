import tkinter as tk
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))   #permite importar desde la raiz del proyecto
from sistema_archivos import obtener_top_jugadores

COLOR_FONDO = "#1a0f1f"                                #colores de la paleta vino tinto y morado
COLOR_PANEL = "#3d1530"
COLOR_PANEL2 = "#5e1f3d"
COLOR_BOTON = "#7b1e3a"
COLOR_ACENTO = "#9b4f7f"
COLOR_TEXTO = "#e8d5e0"

class RankingsView:
    def __init__(self, root, callback_volver):
        self.root = root                                  #ventana principal
        self.callback_volver = callback_volver            #funcion para volver al menu

        self.frame = tk.Frame(root, bg=COLOR_FONDO)       #crea el frame principal
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        tk.Label(
            self.frame,
            text="Top Jugadores",
            font=("Georgia", 22, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO
        ).pack(pady=20)

        top_defensores, top_atacantes = obtener_top_jugadores()   #lee los rankings del json

        self._panel_ranking("Top Defensores", top_defensores, "victorias_defensor", COLOR_PANEL)
        self._panel_ranking("Top Atacantes", top_atacantes, "victorias_atacante", COLOR_PANEL2)

        tk.Button(
            self.frame,
            text="Volver",
            font=("Georgia", 12, "bold"),
            bg=COLOR_BOTON,
            fg=COLOR_TEXTO,
            command=self._volver,
            padx=20, pady=8
        ).pack(pady=20)

    def _panel_ranking(self, titulo, jugadores, campo_victorias, color):
        panel = tk.Frame(self.frame, bg=color, padx=20, pady=15)   #panel de uno de los dos rankings
        panel.pack(pady=10, padx=40, fill="x")

        tk.Label(
            panel,
            text=titulo,
            font=("Georgia", 14, "bold"),
            bg=color,
            fg=COLOR_ACENTO
        ).pack(pady=5)

        if not jugadores:                                            #si aun no hay datos registrados
            tk.Label(
                panel,
                text="Aun no hay jugadores registrados",
                bg=color,
                fg=COLOR_TEXTO,
                font=("Georgia", 11)
            ).pack()
            return

        for i, jugador in enumerate(jugadores):                       #recorre el top 5 de jugadores
            linea = tk.Frame(panel, bg=color)
            linea.pack(fill="x", pady=2)

            tk.Label(
                linea,
                text=f"{i+1}.  {jugador['nombre']}",                  #posicion y nombre del jugador
                font=("Georgia", 12),
                bg=color,
                fg=COLOR_TEXTO,
                anchor="w"
            ).pack(side="left", padx=5)

            tk.Label(
                linea,
                text=f"{jugador[campo_victorias]} victorias",          #cantidad de victorias
                font=("Georgia", 12, "bold"),
                bg=color,
                fg=COLOR_ACENTO,
                anchor="e"
            ).pack(side="right", padx=5)

    def _volver(self):
        self.frame.destroy()                                          #cierra esta pantalla
        self.callback_volver()                                        #vuelve al menu principal  