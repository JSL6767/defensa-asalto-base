import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#Las 3 facciones disponibles con su color y descripción
FACCIONES = {
    "Reino":  {"color": "#c9a84c", "descripcion": "Caballeros y castillos"},
    "Oscura": {"color": "#7b2d8b", "descripcion": "Nigromantes y no-muertos"},
    "Bosque": {"color": "#2d8b3b", "descripcion": "Elfos y naturaleza"}
}

class SeleccionFaccionView:
    def __init__(self, root, jugador1, jugador2, callback):
        self.root = root
        self.jugador1 = jugador1    # datos del jugador 1
        self.jugador2 = jugador2    # datos del jugador 2
        self.callback = callback    # función que se llama al continuar
        self.faccion1 = None        # facción elegida por jugador 1
        self.faccion2 = None        # facción elegida por jugador 2

        self.frame = tk.Frame(root, bg="#1a1a2e")
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        #Titulo de la ventana
        tk.Label(
            self.frame,
            text="⚔ Selección de Facciones ⚔",
            font=("Arial", 20, "bold"),
            bg="#1a1a2e",
            fg="#c9a84c"
        ).pack(pady=20)

        # Panel de selección para cada jugador
        self._panel_faccion(self.jugador1["nombre"], "#16213e", 1)
        self._panel_faccion(self.jugador2["nombre"], "#0f3460", 2)

        # Botón para continuar, deshabilitado hasta que ambos elijan
        self.btn_continuar = tk.Button(
            self.frame,
            text="Continuar",
            font=("Arial", 13, "bold"),
            bg="#c9a84c",
            fg="#1a1a2e",
            state="disabled",
            command=self._continuar,
            padx=20, pady=8
        )
        self.btn_continuar.pack(pady=25)
        
    def _panel_faccion(self, nombre_jugador, color, numero):
        panel = tk.Frame(self.frame, bg=color, padx=20, pady=15)
        panel.pack(pady=8, padx=40, fill="x")

        tk.Label(
            panel,
            text=f"{nombre_jugador} — elige tu facción:",
            font=("Arial", 12, "bold"),
            bg=color, fg="white"
        ).pack(pady=5)

        # Botones de las facciones
        frame_botones = tk.Frame(panel, bg=color)
        frame_botones.pack()

        for nombre_faccion, datos in FACCIONES.items():
            tk.Button(
                frame_botones,
                text=f"{nombre_faccion}\n{datos['descripcion']}",
                font=("Arial", 10),
                bg=datos["color"],
                fg="white",
                width=18,
                command=lambda f=nombre_faccion, n=numero: self._elegir_faccion(f, n)
            ).pack(side="left", padx=8)

        # Label que muestra la facción elegida
        if numero == 1:
            self.label_faccion1 = tk.Label(panel, text="Sin seleccionar", bg=color, fg="#ff6b6b", font=("Arial", 10))
            self.label_faccion1.pack(pady=5)
        else:
            self.label_faccion2 = tk.Label(panel, text="Sin seleccionar", bg=color, fg="#ff6b6b", font=("Arial", 10))
            self.label_faccion2.pack(pady=5)

    def _elegir_faccion(self, faccion, numero):
        #Revisa que los jugadores no elijan la misma facción
        if numero == 1:
            if faccion == self.faccion2:
                messagebox.showerror("Error", "Ambos jugadores no pueden usar la misma facción.")
                return
            self.faccion1 = faccion
            self.label_faccion1.config(text=f"✔ {faccion}", fg="#6bff6b")
        else:
            if faccion == self.faccion1:
                messagebox.showerror("Error", "Ambos jugadores no pueden usar la misma facción.")
                return
            self.faccion2 = faccion
            self.label_faccion2.config(text=f"✔ {faccion}", fg="#6bff6b")

        # Habilita el botón cuando ambos eligieron
        if self.faccion1 and self.faccion2:
            self.btn_continuar.config(state="normal")

    def _continuar(self):
        # Destruye esta ventana y llama al siguiente paso del juego
        self.frame.destroy()
        self.callback(self.jugador1, self.jugador2, self.faccion1, self.faccion2)


