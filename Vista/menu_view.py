import tkinter as tk
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#Se importan los rankings
from Vista.rankings_view import RankingsView

class MenuView:
    def __init__(self, root, jugador1, jugador2, callback_jugar):
        self.root = root
        self.jugador1 = jugador1              #datos del jugador 1
        self.jugador2 = jugador2              #datos del jugador 2
        self.callback_jugar = callback_jugar  #función para iniciar la partida

        #Frame principal
        self.frame = tk.Frame(root, bg="#1a1a2e")
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        #Título del juego
        tk.Label(
            self.frame,
            text="⚔ Defensa y Asalto de Base ⚔",
            font=("Arial", 22, "bold"),
            bg="#1a1a2e",
            fg="#c9a84c"
        ).pack(pady=30)

        #Muestra los nombres de los jugadores conectados
        tk.Label(
            self.frame,
            text=f"{self.jugador1['nombre']}  vs  {self.jugador2['nombre']}",
            font=("Arial", 14),
            bg="#1a1a2e",
            fg="white"
        ).pack(pady=10)

        #Botón para iniciar partida
        tk.Button(
            self.frame,
            text="Nueva Partida",
            font=("Arial", 13, "bold"),
            bg="#c9a84c",
            fg="#1a1a2e",
            command=self._iniciar_partida,
            padx=30, pady=12,
            width=20
        ).pack(pady=15)

        #Botón para ver el ranking
        tk.Button(
            self.frame,
            text="Ver Rankings",
            font=("Arial", 13, "bold"),
            bg="#16213e",
            fg="white",
            command=self._ver_rankings,
            padx=30, pady=12,
            width=20
        ).pack(pady=10)

        #Botón para salir del juego
        tk.Button(
            self.frame,
            text="Salir",
            font=("Arial", 13, "bold"),
            bg="#e94560",
            fg="white",
            command=self.root.quit,
            padx=30, pady=12,
            width=20
        ).pack(pady=10)

    def _iniciar_partida(self):
        #Cierra el menú y pasa a la selección de facciones
        self.frame.destroy()
        self.callback_jugar(self.jugador1, self.jugador2)

    def _ver_rankings(self):
        #Cierra el menú y abre rankings
        self.frame.destroy()
        RankingsView(self.root, self._volver_al_menu)

    def _volver_al_menu(self):
        #Vuelve a mostrar el menú
        self.frame = tk.Frame(self.root, bg="#1a1a2e")
        self.frame.pack(fill="both", expand=True)
        self._construir_ui()

