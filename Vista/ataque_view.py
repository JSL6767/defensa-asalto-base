import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Clases.unidades import Soldado, Tanque, UnidadRapida
from Clases.torres import TorreBasica, TorrePesada, TorreMagica
from Clases.muro import Muro

TAMANIO_CASILLA = 45
FILAS = 12
COLUMNAS = 12

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
    else:
        color_torre = "#3498db"
        color_muro  = "#7f8c8d"
        color_base  = "#e74c3c"
    return color_torre, color_muro, color_base

class AtaqueView:
    def __init__(self, root, mapa, jugador1, jugador2, faccion1, faccion2, vida_base, callback_combate):
        self.root = root
        self.mapa = mapa
        self.jugador1 = jugador1        # defensor
        self.jugador2 = jugador2        # atacante
        self.faccion1 = faccion1        # facción del defensor
        self.faccion2 = faccion2        # facción del atacante
        self.vida_base = vida_base
        self.callback_combate = callback_combate
        self.unidades = []              # lista de unidades colocadas
        self.seleccion = None           # unidad seleccionada para colocar
        self.dinero = 1000               # dinero del atacante
        self.imagenes = {}
        self._cargar_imagenes()
        self.fila_base = 5
        self.columna_base = 1

        self.frame = tk.Frame(root, bg="#1a1a2e")
        self.frame.pack(fill="both", expand=True)
        self._construir_ui()

    def _construir_ui(self):
        # Título
        tk.Label(
            self.frame,
            text=f"Fase de Ataque — {self.jugador2['nombre']}",
            font=("Arial", 14, "bold"),
            bg="#1a1a2e",
            fg="#e74c3c"
        ).pack(pady=10)

        # Dinero disponible
        self.label_dinero = tk.Label(
            self.frame,
            text=f"Dinero: {self.dinero}",
            font=("Arial", 12),
            bg="#1a1a2e",
            fg="white"
        )
        self.label_dinero.pack()

        # Tienda de unidades
        tienda = tk.Frame(self.frame, bg="#16213e", padx=10, pady=8)
        tienda.pack(fill="x", padx=20)
        tk.Label(tienda, text="Unidades:", bg="#16213e", fg="white", font=("Arial", 11, "bold")).pack(side="left", padx=5)

        tk.Button(tienda, text="Soldado $30", bg="#27ae60", fg="white", font=("Arial", 10),
            command=lambda: self._seleccionar("soldado")).pack(side="left", padx=5)
        tk.Button(tienda, text="Tanque $120", bg="#c0392b", fg="white", font=("Arial", 10),
            command=lambda: self._seleccionar("tanque")).pack(side="left", padx=5)
        tk.Button(tienda, text="Rapida $60", bg="#f39c12", fg="white", font=("Arial", 10),
            command=lambda: self._seleccionar("rapida")).pack(side="left", padx=5)

        # Label de selección actual
        self.label_seleccion = tk.Label(tienda, text="Seleccion: ninguna", bg="#16213e", fg="#c9a84c", font=("Arial", 10))
        self.label_seleccion.pack(side="left", padx=10)

        # Canvas del mapa
        self.canvas = tk.Canvas(
            self.frame,
            width=COLUMNAS * TAMANIO_CASILLA,
            height=FILAS * TAMANIO_CASILLA,
            bg="#2d2d44",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self._click_mapa)

        # Botón para iniciar combate
        tk.Button(
            self.frame,
            text="Iniciar Combate!",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            command=self._iniciar_combate,
            padx=15, pady=8
        ).pack(pady=10)

        self._dibujar_mapa()

    def _seleccionar(self, tipo):
        # Guarda qué unidad quiere colocar el atacante
        self.seleccion = tipo
        self.label_seleccion.config(text=f"Seleccion: {tipo}")

    def _click_mapa(self, evento):
        col = evento.x // TAMANIO_CASILLA
        fila = evento.y // TAMANIO_CASILLA

        if not self.seleccion:
            messagebox.showwarning("Aviso", "Selecciona una unidad primero.")
            return
        if col < COLUMNAS - 3:
            messagebox.showwarning("Aviso", "Solo puedes colocar unidades en las ultimas 3 columnas.")
            return
        if self.mapa[fila][col] is not None:
            messagebox.showwarning("Aviso", "Ya hay algo en esa casilla.")
            return

        # Verificamos el costo
        if self.seleccion == "soldado":
            costo = 30
        elif self.seleccion == "tanque":
            costo = 120
        elif self.seleccion == "rapida":
            costo = 60

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

        # Guardamos posición y la ponemos en el mapa
        unidad.fila = fila
        unidad.columna = col
        self.unidades.append(unidad)
        self.mapa[fila][col] = unidad
        self.dinero -= costo
        self.label_dinero.config(text=f"Dinero: {self.dinero}")
        self._dibujar_mapa()

    def _dibujar_mapa(self):
        self.canvas.delete("all")

        for fila in range(FILAS):
            for col in range(COLUMNAS):
                x1 = col * TAMANIO_CASILLA
                y1 = fila * TAMANIO_CASILLA
                x2 = x1 + TAMANIO_CASILLA
                y2 = y1 + TAMANIO_CASILLA
                objeto = self.mapa[fila][col]
                usar_imagen = False
                imagen = None
                texto = ""

                if fila == self.fila_base and col == self.columna_base:
                    texto = "BASE"
                    if "base" in self.imagenes:
                        usar_imagen = True
                        imagen = self.imagenes["base"]
                elif objeto is None:
                    if col >= COLUMNAS - 3:
                        texto = ""  # zona de ataque
                    else:
                        texto = ""
                elif isinstance(objeto, Muro):
                    texto = "MUR"
                    if "muro" in self.imagenes:
                        usar_imagen = True
                        imagen = self.imagenes["muro"]
                elif isinstance(objeto, TorreBasica):
                    texto = "TBA"
                    if "torre_basica" in self.imagenes:
                        usar_imagen = True
                        imagen = self.imagenes["torre_basica"]
                elif isinstance(objeto, TorrePesada):
                    texto = "TPE"
                    if "torre_pesada" in self.imagenes:
                        usar_imagen = True
                        imagen = self.imagenes["torre_pesada"]
                elif isinstance(objeto, TorreMagica):
                    texto = "TMA"
                    if "torre_magica" in self.imagenes:
                        usar_imagen = True
                        imagen = self.imagenes["torre_magica"]
                elif isinstance(objeto, Soldado):
                    texto = "SOL"
                    if "soldado" in self.imagenes:
                        usar_imagen = True
                        imagen = self.imagenes["soldado"]
                elif isinstance(objeto, Tanque):
                    texto = "TAN"
                    if "tanque" in self.imagenes:
                        usar_imagen = True
                        imagen = self.imagenes["tanque"]
                elif isinstance(objeto, UnidadRapida):
                    texto = "RAP"
                    if "rapida" in self.imagenes:
                        usar_imagen = True
                        imagen = self.imagenes["rapida"]

                # Fondo del mapa
                if fila == self.fila_base and col == self.columna_base:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#2d2d44", outline="#3d3d5c", width=1)
                elif objeto is None and col >= COLUMNAS - 3:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#1a3a1a", outline="#3d3d5c", width=1)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#2d2d44", outline="#3d3d5c", width=1)

                if usar_imagen:
                    self.canvas.create_image(x1, y1, anchor="nw", image=imagen)
                elif texto:
                    self.canvas.create_text(x1+25, y1+25, text=texto, fill="white", font=("Arial", 7, "bold"))
    
    def _iniciar_combate(self):
        if not self.unidades:
            messagebox.showwarning("Aviso", "Debes colocar al menos una unidad.")
            return
        self.frame.destroy()
        self.callback_combate(self.mapa, self.unidades, self.jugador1, self.jugador2, self.faccion1, self.faccion2, self.vida_base)

    def _cargar_imagenes(self):
        from PIL import Image, ImageTk
        import os

        if self.faccion1 == "Reino":
            prefijo_defensor = "reino"
        elif self.faccion1 == "Oscura":
            prefijo_defensor = "oscura"
        elif self.faccion1 == "Bosque":
            prefijo_defensor = "bosque"

        if self.faccion2 == "Reino":
            prefijo_atacante = "reino"
        elif self.faccion2 == "Oscura":
            prefijo_atacante = "oscura"
        elif self.faccion2 == "Bosque":
            prefijo_atacante = "bosque"

        self.imagenes = {}

        # Cargamos imágenes de estructuras del defensor
        tipos_estructuras = ["muro", "torre_basica", "torre_pesada", "torre_magica", "base"]
        for tipo in tipos_estructuras:
            ruta = f"assets/imagenes/{prefijo_defensor}_{tipo}.png"
            if os.path.exists(ruta):
                img = Image.open(ruta).resize((50, 50), Image.NEAREST)
                self.imagenes[tipo] = ImageTk.PhotoImage(img)

        # Cargamos imágenes de unidades del atacante
        tipos_unidades = ["soldado", "tanque", "rapida"]
        for tipo in tipos_unidades:
            ruta = f"assets/imagenes/{prefijo_atacante}_{tipo}.png"
            if os.path.exists(ruta):
                img = Image.open(ruta).resize((50, 50), Image.NEAREST)
                self.imagenes[tipo] = ImageTk.PhotoImage(img)
