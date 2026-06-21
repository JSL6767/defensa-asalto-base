import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

COLOR_FONDO = "#1a0f1f"
COLOR_PANEL = "#3d1530"
COLOR_PANEL2 = "#5e1f3d"
COLOR_ACENTO = "#9b4f7f"
COLOR_TEXTO = "#e8d5e0"

# Las facciones mantienen sus colores propios
FACCIONES = {
    "Reino":  {"color": "#c9a84c", "descripcion": "Caballeros y castillos"},
    "Oscura": {"color": "#7b2d8b", "descripcion": "Nigromantes y no-muertos"},
    "Bosque": {"color": "#2d8b3b", "descripcion": "Elfos y naturaleza"}
}

class SeleccionFaccionView:
    def __init__(self, root, jugador1, jugador2, callback):
        self.root = root
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.callback = callback
        self.faccion1 = None
        self.faccion2 = None

        self.frame = tk.Frame(root, bg=COLOR_FONDO)
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        tk.Label(
            self.frame,
            text="Seleccion de Facciones",
            font=("Georgia", 20, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO
        ).pack(pady=20)

        self._panel_faccion(self.jugador1["nombre"], COLOR_PANEL, 1)
        self._panel_faccion(self.jugador2["nombre"], COLOR_PANEL2, 2)

        self.btn_continuar = tk.Button(
            self.frame,
            text="Continuar",
            font=("Georgia", 13, "bold"),
            bg=COLOR_ACENTO,
            fg=COLOR_FONDO,
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
            text=f"{nombre_jugador} - elige tu faccion:",
            font=("Georgia", 12, "bold"),
            bg=color, fg=COLOR_TEXTO
        ).pack(pady=5)

        frame_botones = tk.Frame(panel, bg=color)
        frame_botones.pack()

        for nombre_faccion, datos in FACCIONES.items():
            tk.Button(
                frame_botones,
                text=f"{nombre_faccion}\n{datos['descripcion']}",
                font=("Georgia", 10),
                bg=datos["color"],
                fg="white",
                width=18,
                command=lambda f=nombre_faccion, n=numero: self._elegir_faccion(f, n)
            ).pack(side="left", padx=8)

        if numero == 1:
            self.label_faccion1 = tk.Label(panel, text="Sin seleccionar", bg=color, fg="#c97b7b", font=("Georgia", 10))
            self.label_faccion1.pack(pady=5)
        else:
            self.label_faccion2 = tk.Label(panel, text="Sin seleccionar", bg=color, fg="#c97b7b", font=("Georgia", 10))
            self.label_faccion2.pack(pady=5)

    def _elegir_faccion(self, faccion, numero):
        if numero == 1:
            if faccion == self.faccion2:
                messagebox.showerror("Error", "Ambos jugadores no pueden usar la misma faccion.")
                return
            self.faccion1 = faccion
            self.label_faccion1.config(text=faccion, fg="#a8c97b")
        else:
            if faccion == self.faccion1:
                messagebox.showerror("Error", "Ambos jugadores no pueden usar la misma faccion.")
                return
            self.faccion2 = faccion
            self.label_faccion2.config(text=faccion, fg="#a8c97b")

        if self.faccion1 and self.faccion2:
            self.btn_continuar.config(state="normal")

    def _continuar(self):
        self.frame.destroy()
        self.callback(self.jugador1, self.jugador2, self.faccion1, self.faccion2)


