import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Clases.unidades import Soldado, Tanque, UnidadRapida

# Tamaño de casilla igual que el mapa
TAMANIO_CASILLA = 50
FILAS = 12
COLUMNAS = 12

class AtaqueView:
    def __init__(self, root, mapa, jugador1, jugador2, faccion1, faccion2, vida_base, callback_combate):
        self.root = root
        self.mapa = mapa                    # mapa con las torres y muros del defensor
        self.jugador1 = jugador1            # defensor
        self.jugador2 = jugador2            # atacante
        self.faccion1 = faccion1
        self.faccion2 = faccion2
        self.vida_base = vida_base          # vida de la base central
        self.callback_combate = callback_combate  # función para iniciar el combate

        # Lista de unidades colocadas por el atacante
        self.unidades = []

        # Elemento seleccionado para colocar
        self.seleccion = None

        # Dinero del atacante
        self.dinero = 200

        self.frame = tk.Frame(root, bg="#1a1a2e")
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        # Título
        tk.Label(
            self.frame,
            text=f"⚔ Fase de Ataque — {self.jugador2['nombre']} (Atacante)",
            font=("Arial", 14, "bold"),
            bg="#1a1a2e",
            fg="#e74c3c"
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

        # Tienda de unidades
        self._construir_tienda()

        # Canvas del mapa
        self.canvas = tk.Canvas(
            self.frame,
            width=COLUMNAS * TAMANIO_CASILLA,
            height=FILAS * TAMANIO_CASILLA,
            bg="#2d2d44",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        # Click para colocar unidades
        self.canvas.bind("<Button-1>", self._click_mapa)

        # Botón para iniciar el combate
        tk.Button(
            self.frame,
            text="¡Iniciar Combate!",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            command=self._iniciar_combate,
            padx=15, pady=8
        ).pack(pady=10)

        # Dibujamos el mapa con las torres ya colocadas
        self._dibujar_mapa()

    def _construir_tienda(self):
        tienda = tk.Frame(self.frame, bg="#16213e", padx=10, pady=8)
        tienda.pack(fill="x", padx=20)

        tk.Label(tienda, text="Unidades:", bg="#16213e", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=5)

        # Botones de compra de unidades
        elementos = [
            ("Soldado $30",       "soldado",  "#27ae60"),
            ("Tanque $120",       "tanque",   "#c0392b"),
            ("Rapida $60",        "rapida",   "#f39c12"),
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

        # Label de selección actual
        self.label_seleccion = tk.Label(tienda, text="Seleccion: ninguna", bg="#16213e", fg="#c9a84c", font=("Arial", 10))
        self.label_seleccion.pack(side="left", padx=10)

    def _seleccionar(self, tipo):
        # Guarda qué unidad quiere colocar el atacante
        self.seleccion = tipo
        self.label_seleccion.config(text=f"Seleccion: {tipo}")

    def _click_mapa(self, evento):
        # Calcula en qué casilla hizo click
        col = evento.x // TAMANIO_CASILLA
        fila = evento.y // TAMANIO_CASILLA

        if not self.seleccion:
            messagebox.showwarning("Aviso", "Selecciona una unidad primero.")
            return

        # Las unidades solo se pueden colocar en las últimas 3 columnas
        if col < COLUMNAS - 3:
            messagebox.showwarning("Aviso", "Solo puedes colocar unidades en las ultimas 3 columnas.")
            return

        # No se puede colocar sobre torres o muros
        if self.mapa[fila][col] is not None:
            messagebox.showwarning("Aviso", "Ya hay algo en esa casilla.")
            return

        # Verificamos el costo
        costos = {"soldado": 30, "tanque": 120, "rapida": 60}
        costo = costos[self.seleccion]

        if self.dinero < costo:
            messagebox.showerror("Sin dinero", "No tienes suficiente dinero.")
            return

        # Creamos la unidad según la selección
        if self.seleccion == "soldado":
            unidad = Soldado()
        elif self.seleccion == "tanque":
            unidad = Tanque()
        elif self.seleccion == "rapida":
            unidad = UnidadRapida()

        # Guardamos posición
        unidad.fila = fila
        unidad.columna = col
        self.unidades.append(unidad)
        self.mapa[fila][col] = unidad

        # Descontamos el dinero
        self.dinero -= costo
        self.label_dinero.config(text=f"💰 Dinero: {self.dinero}")

        self._dibujar_mapa()

    def _dibujar_mapa(self):
        from Clases.torres import TorreBasica, TorrePesada, TorreMagica
        from Clases.muro import Muro

        self.canvas.delete("all")

        for fila in range(FILAS):
            for col in range(COLUMNAS):
                x1 = col * TAMANIO_CASILLA
                y1 = fila * TAMANIO_CASILLA
                x2 = x1 + TAMANIO_CASILLA
                y2 = y1 + TAMANIO_CASILLA

                objeto = self.mapa[fila][col]

                # Color según el contenido
                if fila == 5 and col == 1:
                    color = "#e74c3c"    # base
                    texto = "BASE"
                elif objeto is None:
                    # Zona de ataque destacada
                    if col >= COLUMNAS - 3:
                        color = "#1a3a1a"  # zona donde puede colocar unidades
                    else:
                        color = "#2d2d44"  # zona normal
                    texto = ""
                elif isinstance(objeto, Muro):
                    color = "#7f8c8d"
                    texto = "MUR"
                elif isinstance(objeto, TorreBasica):
                    color = "#3498db"
                    texto = "TBA"
                elif isinstance(objeto, TorrePesada):
                    color = "#e67e22"
                    texto = "TPE"
                elif isinstance(objeto, TorreMagica):
                    color = "#9b59b6"
                    texto = "TMA"
                elif isinstance(objeto, Soldado):
                    color = "#27ae60"
                    texto = "SOL"
                elif isinstance(objeto, Tanque):
                    color = "#c0392b"
                    texto = "TAN"
                elif isinstance(objeto, UnidadRapida):
                    color = "#f39c12"
                    texto = "RAP"
                else:
                    color = "#2d2d44"
                    texto = ""

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#1a1a2e", width=1)
                if texto:
                    self.canvas.create_text(x1+25, y1+25, text=texto, fill="white", font=("Arial", 7, "bold"))

    def _iniciar_combate(self):
        if not self.unidades:
            messagebox.showwarning("Aviso", "Debes colocar al menos una unidad.")
            return

        # Pasa el mapa y las unidades al combate
        self.frame.destroy()
        self.callback_combate(self.mapa, self.unidades, self.jugador1, self.jugador2, self.faccion1, self.faccion2, self.vida_base)