import tkinter as tk
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#Se importa la función que retorna los top 5
from sistema_archivos import obtener_top_jugadores

class RankingsView:
    def __init__(self, root, callback_volver):
        self.root = root
        self.callback_volver = callback_volver  # función para volver al menú anterior

        #Frame principal con fondo oscuro
        self.frame = tk.Frame(root, bg="#1a1a2e")
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        #Título de la ventana
        tk.Label(
            self.frame,
            text="🏆 Top Jugadores 🏆",
            font=("Arial", 22, "bold"),
            bg="#1a1a2e",
            fg="#c9a84c"
        ).pack(pady=20)

        #Se obtienen los top 5 desde el archivo JSON
        top_defensores, top_atacantes = obtener_top_jugadores()

        #Se crea un panel para defensores y otro para atacantes
        self._panel_ranking("Top Defensores 🛡", top_defensores, "victorias_defensor", "#16213e")
        self._panel_ranking("Top Atacantes ⚔", top_atacantes, "victorias_atacante", "#0f3460")

        #Botón para volver al menú anterior
        tk.Button(
            self.frame,
            text="Volver",
            font=("Arial", 12, "bold"),
            bg="#e94560",
            fg="white",
            command=self._volver,
            padx=20, pady=8
        ).pack(pady=20)

    def _panel_ranking(self, titulo, jugadores, campo_victorias, color):
        #Panel con el color recibido
        panel = tk.Frame(self.frame, bg=color, padx=20, pady=15)
        panel.pack(pady=10, padx=40, fill="x")

        #Título del panel
        tk.Label(
            panel,
            text=titulo,
            font=("Arial", 14, "bold"),
            bg=color,
            fg="#c9a84c"
        ).pack(pady=5)

        #Si no hay jugadores no se muestra el mensaje
        if not jugadores:
            tk.Label(
                panel,
                text="Aún no hay jugadores registrados",
                bg=color,
                fg="white",
                font=("Arial", 11)
            ).pack()
            return

        #Se recorre la lista y se muestra su jugador con su posición
        for i, jugador in enumerate(jugadores):
            linea = tk.Frame(panel, bg=color)
            linea.pack(fill="x", pady=2)

            #Medallas según posición
            medalla = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][i]

            #Nombre del jugador a la izquierda
            tk.Label(
                linea,
                text=f"{medalla}  {jugador['nombre']}",
                font=("Arial", 12),
                bg=color,
                fg="white",
                anchor="w"
            ).pack(side="left", padx=5)

            #Victorias a la derecha
            tk.Label(
                linea,
                text=f"{jugador[campo_victorias]} victorias",
                font=("Arial", 12, "bold"),
                bg=color,
                fg="#c9a84c",
                anchor="e"
            ).pack(side="right", padx=5)

    def _volver(self):
        #Destruye este frame y llama al callback para volver al menú
        self.frame.destroy()
        self.callback_volver()

