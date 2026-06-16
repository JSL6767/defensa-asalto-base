import tkinter as tk
from sistema_archivos import actualizar_victorias
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class FinPartidaView:
    def __init__(self, root, ganador_rol, jugador1, jugador2, victorias_defensor, victorias_atacante, callback_volver):
        self.root = root
        self.ganador_rol = ganador_rol  #defensor o atacante
        self.jugador1 = jugador1                 
        self.jugador2 = jugador2                       
        self.victorias_defensor = victorias_defensor   
        self.victorias_atacante = victorias_atacante    
        self.callback_volver = callback_volver          # función para volver al menú

        #actualiza victorias en el JSON
        if ganador_rol == "defensor":
            actualizar_victorias(jugador1["nombre"], "defensor")
        else:
            actualizar_victorias(jugador2["nombre"], "atacante")

        self.frame = tk.Frame(root, bg="#1a1a2e")
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        #nombre de ganador según su rol
        if self.ganador_rol == "defensor":
            nombre_ganador = self.jugador1["nombre"]
            color = "#3498db"
            emoji = "🛡"
        else:
            nombre_ganador = self.jugador2["nombre"]
            color = "#e74c3c"
            emoji = "⚔"

        #título
        tk.Label(
            self.frame,
            text="🏆 Fin de Partida 🏆",
            font=("Arial", 22, "bold"),
            bg="#1a1a2e",
            fg="#c9a84c"
        ).pack(pady=30)

        #ganador
        tk.Label(
            self.frame,
            text=f"{emoji} {nombre_ganador} gana la partida! {emoji}",
            font=("Arial", 16, "bold"),
            bg="#1a1a2e",
            fg=color
        ).pack(pady=10)

        #resultado
        panel = tk.Frame(self.frame, bg="#16213e", padx=30, pady=20)
        panel.pack(pady=20, padx=40, fill="x")

        tk.Label(
            panel,
            text="Resultado Final",
            font=("Arial", 14, "bold"),
            bg="#16213e",
            fg="#c9a84c"
        ).pack(pady=5)

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

        #botón volver al menú
        tk.Button(
            self.frame,
            text="Volver al Menú",
            font=("Arial", 13, "bold"),
            bg="#c9a84c",
            fg="#1a1a2e",
            command=self._volver,
            padx=20, pady=10
        ).pack(pady=30)

    def _volver(self):
        #cierra esta ventana para volver al menú
        self.frame.destroy()
        self.callback_volver()

    

