import tkinter as tk
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))   #permite importar desde la raiz del proyecto
from Vista.rankings_view import RankingsView

COLOR_FONDO = "#1a0f1f"                                #colores de la paleta vino tinto y morado
COLOR_PANEL = "#3d1530"
COLOR_BOTON_PRINCIPAL = "#5e2750"
COLOR_BOTON_SALIR = "#7b1e3a"
COLOR_ACENTO = "#9b4f7f"
COLOR_TEXTO = "#e8d5e0"

class MenuView:
    def __init__(self, root, jugador1, jugador2, callback_jugar):
        self.root = root                                   #ventana principal
        self.jugador1 = jugador1                           #defensor
        self.jugador2 = jugador2                           #atacante
        self.callback_jugar = callback_jugar               #funcion para iniciar una partida nueva

        self.frame = tk.Frame(root, bg=COLOR_FONDO)        #crea el frame principal
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        tk.Label(
            self.frame,
            text="Defensa y Asalto de Base",
            font=("Georgia", 22, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO
        ).pack(pady=30)

        tk.Label(
            self.frame,
            text=f"{self.jugador1['nombre']}  contra  {self.jugador2['nombre']}",   #muestra los jugadores conectados
            font=("Georgia", 14),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        ).pack(pady=10)

        tk.Button(
            self.frame,
            text="Nueva Partida",
            font=("Georgia", 13, "bold"),
            bg=COLOR_ACENTO,
            fg=COLOR_FONDO,
            command=self._iniciar_partida,
            padx=30, pady=12,
            width=20
        ).pack(pady=15)

        tk.Button(
            self.frame,
            text="Ver Rankings",
            font=("Georgia", 13, "bold"),
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO,
            command=self._ver_rankings,
            padx=30, pady=12,
            width=20
        ).pack(pady=10)

        tk.Button(
            self.frame,
            text="Salir",
            font=("Georgia", 13, "bold"),
            bg=COLOR_BOTON_SALIR,
            fg=COLOR_TEXTO,
            command=self.root.quit,                          #cierra el programa completo
            padx=30, pady=12,
            width=20
        ).pack(pady=10)

    def _iniciar_partida(self):
        self.frame.destroy()                                  #cierra el menu
        self.callback_jugar(self.jugador1, self.jugador2)      #pasa a la seleccion de facciones

    def _ver_rankings(self):
        self.frame.destroy()                                  #cierra el menu
        RankingsView(self.root, self._volver_al_menu)          #abre la pantalla de rankings

    def _volver_al_menu(self):
        self.frame = tk.Frame(self.root, bg=COLOR_FONDO)       #vuelve a crear el frame del menu
        self.frame.pack(fill="both", expand=True)
        self._construir_ui()