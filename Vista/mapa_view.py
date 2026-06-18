import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Clases.torres import TorreBasica, TorrePesada, TorreMagica
from Clases.muro import Muro

# Tamaño de cada casilla en píxeles
TAMANIO_CASILLA = 45
FILAS = 12
COLUMNAS = 12

# Colores según el contenido de la casilla
COLORES = {
    "vacio":   "#2d2d44",  # casilla vacía
    "base":    "#e74c3c",  # base central del defensor
    "muro":    "#7f8c8d",  # muro
    "torre_basica":  "#3498db",  # torre básica
    "torre_pesada":  "#e67e22",  # torre pesada
    "torre_magica":  "#9b59b6",  # torre mágica
    "unidad":  "#e74c3c",  # unidades atacantes
}
def obtener_colores_faccion(faccion):
        # Retorna color de torre, muro y base según la facción
            if faccion == "Reino":
                color_torre = "#c9a84c"
                color_muro  = "#a07830"
                color_base  = "#c9a84c"
            elif faccion == "Oscura":
                color_torre = "#7b2d8b"
                color_muro  = "#4a1a5a"
                color_base  = "#7b2d8b"
            elif faccion == "Bosque":
                color_torre = "#2d8b3b"
                color_muro  = "#1a5a25"
                color_base  = "#2d8b3b"
            return color_torre, color_muro, color_base
class MapaView:
    def __init__(self, root, jugador1, jugador2, faccion1, faccion2, callback_fin_construccion):
        self.root = root
        self.jugador1 = jugador1        # defensor
        self.jugador2 = jugador2        # atacante
        self.faccion1 = faccion1        # facción del defensor
        self.faccion2 = faccion2        # facción del atacante
        self.callback_fin_construccion = callback_fin_construccion  # cuando termina de construir

        # Matriz 12x12 que representa el mapa, None = vacío
        self.mapa = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]

        # La base central está fija en el centro izquierdo
        self.fila_base = 5
        self.columna_base = 1
        self.vida_base = 500

        # Elemento seleccionado para colocar
        self.seleccion = None

        # Dinero del defensor
        self.dinero = 1000

        self.frame = tk.Frame(root, bg="#1a1a2e")
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        # Título
        tk.Label(
            self.frame,
            text=f"⚔ Fase de Construcción — {self.jugador1['nombre']} (Defensor)",
            font=("Arial", 14, "bold"),
            bg="#1a1a2e",
            fg="#c9a84c"
        ).pack(pady=10)

        # Dinero disponible
        self.label_dinero = tk.Label(
            self.frame,
            text=f"💰 Dinero: {self.dinero}",
            font=("Arial", 12),
            bg="#1a1a2e",
            fg="white"
        )
        self.label_dinero.pack()

        # Panel de tienda (botones para comprar)
        self._construir_tienda()

        # Canvas donde se dibuja el mapa
        self.canvas = tk.Canvas(
            self.frame,
            width=COLUMNAS * TAMANIO_CASILLA,
            height=FILAS * TAMANIO_CASILLA,
            bg="#2d2d44",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        # Click en el canvas para colocar elementos
        self.canvas.bind("<Button-1>", self._click_mapa)

        # Botón para terminar construcción
        tk.Button(
            self.frame,
            text="Terminar Construcción",
            font=("Arial", 12, "bold"),
            bg="#c9a84c",
            fg="#1a1a2e",
            command=self._terminar_construccion,
            padx=15, pady=8
        ).pack(pady=10)

        # Dibujamos el mapa inicial
        self._dibujar_mapa()

    def _construir_tienda(self):
        # Panel de tienda con los elementos disponibles
        tienda = tk.Frame(self.frame, bg="#16213e", padx=10, pady=8)
        tienda.pack(fill="x", padx=20)

        tk.Label(tienda, text="Tienda:", bg="#16213e", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=5)

        # Botones de compra
        elementos = [
            ("Muro $20",         "muro",         "#7f8c8d"),
            ("Torre Básica $50", "torre_basica",  "#3498db"),
            ("Torre Pesada $150","torre_pesada",  "#e67e22"),
            ("Torre Mágica $100","torre_magica",  "#9b59b6"),
        ]

        for nombre, tipo, color in elementos:
            tk.Button(
                tienda,
                text=nombre,
                bg=color,
                fg="white",
                font=("Arial", 10),
                command=lambda t=tipo: self._seleccionar(t)
            ).pack(side="left", padx=5)

        # Label que muestra qué está seleccionado
        self.label_seleccion = tk.Label(tienda, text="Selección: ninguna", bg="#16213e", fg="#c9a84c", font=("Arial", 10))
        self.label_seleccion.pack(side="left", padx=10)

    def _seleccionar(self, tipo):
        # Guarda qué elemento quiere colocar el defensor
        self.seleccion = tipo
        self.label_seleccion.config(text=f"Selección: {tipo}")

    def _click_mapa(self, evento):
        # Calcula en qué casilla hizo click
        col = evento.x // TAMANIO_CASILLA
        fila = evento.y // TAMANIO_CASILLA

        # No se puede colocar nada si no hay selección
        if not self.seleccion:
            messagebox.showwarning("Aviso", "Selecciona un elemento de la tienda primero.")
            return

        # No se puede colocar sobre la base
        if fila == self.fila_base and col == self.columna_base:
            messagebox.showwarning("Aviso", "No puedes colocar nada sobre la base.")
            return

        # No se puede colocar sobre algo que ya existe
        if self.mapa[fila][col] is not None:
            messagebox.showwarning("Aviso", "Ya hay algo en esa casilla.")
            return

        # Verificamos el costo y descontamos el dinero
        costos = {"muro": 20, "torre_basica": 50, "torre_pesada": 150, "torre_magica": 100}
        costo = costos[self.seleccion]

        if self.dinero < costo:
            messagebox.showerror("Sin dinero", "No tienes suficiente dinero.")
            return

        # Creamos el objeto según la selección
        if self.seleccion == "muro":
            objeto = Muro()
        elif self.seleccion == "torre_basica":
            objeto = TorreBasica()
        elif self.seleccion == "torre_pesada":
            objeto = TorrePesada()
        elif self.seleccion == "torre_magica":
            objeto = TorreMagica()

        # Guardamos posición y lo ponemos en el mapa
        objeto.fila = fila
        objeto.columna = col
        self.mapa[fila][col] = objeto

        # Descontamos el dinero y actualizamos el label
        self.dinero -= costo
        self.label_dinero.config(text=f"💰 Dinero: {self.dinero}")

        # Redibujamos el mapa
        self._dibujar_mapa()
    
    def _dibujar_mapa(self):
        self.canvas.delete("all")
        # Obtenemos los colores de la facción del defensor
        color_torre, color_muro, color_base = obtener_colores_faccion(self.faccion1)

        for fila in range(FILAS):
            for col in range(COLUMNAS):
                x1 = col * TAMANIO_CASILLA
                y1 = fila * TAMANIO_CASILLA
                x2 = x1 + TAMANIO_CASILLA
                y2 = y1 + TAMANIO_CASILLA

                if fila == self.fila_base and col == self.columna_base:
                    color = color_base
                    texto = "BASE"
                elif self.mapa[fila][col] is not None:
                    objeto = self.mapa[fila][col]
                    if isinstance(objeto, Muro):
                        color = color_muro
                        texto = "MUR"
                    else:
                        color = color_torre
                        texto = objeto.nombre[:3].upper()
                else:
                    color = "#2d2d44"
                    texto = ""

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#1a1a2e", width=1)
                if texto:
                    self.canvas.create_text(x1+25, y1+25, text=texto, fill="white", font=("Arial", 7, "bold"))

    def _terminar_construccion(self):
        # Termina la fase de construcción y pasa a la fase de ataque
        self.frame.destroy()
        self.callback_fin_construccion(self.mapa, self.jugador1, self.jugador2, self.faccion1, self.faccion2, self.vida_base)
    