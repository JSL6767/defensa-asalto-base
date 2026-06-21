import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Clases.unidades import Soldado, Tanque, UnidadRapida
from Clases.torres import TorreBasica, TorrePesada, TorreMagica
from Clases.muro import Muro

TAMANIO_CASILLA = 50
FILAS = 12
COLUMNAS = 12

COLOR_FONDO = "#1a0f1f"
COLOR_PANEL = "#3d1530"
COLOR_CASILLA = "#3d1530"
COLOR_ZONA_ATAQUE = "#5e1f3d"
COLOR_BORDE = "#5e1f3d"
COLOR_ACENTO = "#9b4f7f"
COLOR_TEXTO = "#e8d5e0"

class AtaqueView:
    def __init__(self, root, mapa, jugador1, jugador2, faccion1, faccion2, vida_base, callback_combate, dinero_extra=0, dinero_defensor=500):
        self.root = root
        self.mapa = mapa
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.faccion1 = faccion1
        self.faccion2 = faccion2
        self.vida_base = vida_base
        self.callback_combate = callback_combate
        self.unidades = []
        self.seleccion = None
        self.dinero = dinero_extra if dinero_extra > 0 else 300
        self.dinero_defensor = dinero_defensor

        self.imagenes = {}
        self._cargar_imagenes()
        self.fila_base = 5
        self.columna_base = 1

        self.frame = tk.Frame(root, bg=COLOR_FONDO)
        self.frame.pack(fill="both", expand=True)
        self._construir_ui()

    def _construir_ui(self):
        tk.Label(
            self.frame,
            text=f"Fase de Ataque - {self.jugador2['nombre']}",
            font=("Georgia", 14, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_ACENTO
        ).pack(pady=10)

        self.label_dinero = tk.Label(
            self.frame,
            text=f"Dinero: {self.dinero}",
            font=("Georgia", 12),
            bg=COLOR_FONDO,
            fg=COLOR_TEXTO
        )
        self.label_dinero.pack()

        tienda = tk.Frame(self.frame, bg=COLOR_PANEL, padx=10, pady=8)
        tienda.pack(fill="x", padx=20)
        tk.Label(tienda, text="Unidades:", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=("Georgia", 11, "bold")).pack(side="left", padx=5)

        tk.Button(tienda, text="Soldado $30", bg="#27ae60", fg="white", font=("Georgia", 10),
            command=lambda: self._seleccionar("soldado")).pack(side="left", padx=5)
        tk.Button(tienda, text="Tanque $120", bg="#c0392b", fg="white", font=("Georgia", 10),
            command=lambda: self._seleccionar("tanque")).pack(side="left", padx=5)
        tk.Button(tienda, text="Rapida $60", bg="#f39c12", fg="white", font=("Georgia", 10),
            command=lambda: self._seleccionar("rapida")).pack(side="left", padx=5)

        self.label_seleccion = tk.Label(tienda, text="Seleccion: ninguna", bg=COLOR_PANEL, fg=COLOR_ACENTO, font=("Georgia", 10))
        self.label_seleccion.pack(side="left", padx=10)

        tk.Label(
            self.frame,
            text="Clic izquierdo para añadir, clic derecho para borrar",
            font=("Georgia", 9),
            bg=COLOR_FONDO,
            fg="#9b7d8f"
        ).pack(pady=(2, 0))

        self.canvas = tk.Canvas(
            self.frame,
            width=COLUMNAS * TAMANIO_CASILLA,
            height=FILAS * TAMANIO_CASILLA,
            bg=COLOR_FONDO,
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        self.canvas.bind("<Button-1>", self._click_mapa)
        self.canvas.bind("<Button-3>", self._click_derecho)

        tk.Button(
            self.frame,
            text="Iniciar Combate",
            font=("Georgia", 12, "bold"),
            bg=COLOR_ACENTO,
            fg=COLOR_FONDO,
            command=self._iniciar_combate,
            padx=15, pady=8
        ).pack(pady=10)

        self._dibujar_mapa()

    def _seleccionar(self, tipo):
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

        if self.seleccion == "soldado":
            costo = 30
        elif self.seleccion == "tanque":
            costo = 120
        elif self.seleccion == "rapida":
            costo = 60

        if self.dinero < costo:
            messagebox.showerror("Sin dinero", "No tienes suficiente dinero.")
            return

        if self.seleccion == "soldado":
            unidad = Soldado()
        elif self.seleccion == "tanque":
            unidad = Tanque()
        elif self.seleccion == "rapida":
            unidad = UnidadRapida()

        unidad.fila = fila
        unidad.columna = col
        self.unidades.append(unidad)
        self.mapa[fila][col] = unidad
        self.dinero -= costo
        self.label_dinero.config(text=f"Dinero: {self.dinero}")
        self._dibujar_mapa()

    def _click_derecho(self, evento):
        col = evento.x // TAMANIO_CASILLA
        fila = evento.y // TAMANIO_CASILLA

        objeto = self.mapa[fila][col]
        if objeto is None:
            return

        if isinstance(objeto, Soldado):
            costo = 30
        elif isinstance(objeto, Tanque):
            costo = 120
        elif isinstance(objeto, UnidadRapida):
            costo = 60
        else:
            return

        self.mapa[fila][col] = None
        self.unidades.remove(objeto)
        self.dinero += costo
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

                if objeto is None and fila != self.fila_base and col >= COLUMNAS - 3:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_ZONA_ATAQUE, outline=COLOR_BORDE, width=1)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_CASILLA, outline=COLOR_BORDE, width=1)

                if usar_imagen:
                    self.canvas.create_image(x1, y1, anchor="nw", image=imagen)
                elif texto:
                    self.canvas.create_text(x1+25, y1+25, text=texto, fill=COLOR_TEXTO, font=("Georgia", 7, "bold"))

    def _iniciar_combate(self):
        if not self.unidades:
            messagebox.showwarning("Aviso", "Debes colocar al menos una unidad.")
            return
        self.frame.destroy()
        self.callback_combate(self.mapa, self.unidades, self.jugador1, self.jugador2, self.faccion1, self.faccion2, self.vida_base, self.dinero_defensor, self.dinero)

    def _cargar_imagenes(self):
        from PIL import Image, ImageTk

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

        tipos_estructuras = ["muro", "torre_basica", "torre_pesada", "torre_magica", "base"]
        for tipo in tipos_estructuras:
            ruta = f"assets/imagenes/{prefijo_defensor}_{tipo}.png"
            if os.path.exists(ruta):
                img = Image.open(ruta).resize((50, 50), Image.NEAREST)
                self.imagenes[tipo] = ImageTk.PhotoImage(img)

        tipos_unidades = ["soldado", "tanque", "rapida"]
        for tipo in tipos_unidades:
            ruta = f"assets/imagenes/{prefijo_atacante}_{tipo}.png"
            if os.path.exists(ruta):
                img = Image.open(ruta).resize((50, 50), Image.NEAREST)
                self.imagenes[tipo] = ImageTk.PhotoImage(img)