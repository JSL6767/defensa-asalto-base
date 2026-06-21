import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Clases.torres import TorreBasica, TorrePesada, TorreMagica
from Clases.muro import Muro

TAMANIO_CASILLA = 50
FILAS = 12
COLUMNAS = 12

COLOR_FONDO = "#1a0f1f"
COLOR_PANEL = "#3d1530"
COLOR_CASILLA = "#3d1530"
COLOR_BORDE = "#5e1f3d"
COLOR_ACENTO = "#9b4f7f"
COLOR_TEXTO = "#e8d5e0"

class MapaView:
    def __init__(self, root, jugador1, jugador2, faccion1, faccion2, callback_fin_construccion, dinero_extra=0):
        self.root = root
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.faccion1 = faccion1
        self.faccion2 = faccion2
        self.callback_fin_construccion = callback_fin_construccion

        self.mapa = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]
        self.fila_base = 5
        self.columna_base = 1
        self.vida_base = 500
        self.seleccion = None
        self.dinero = 200 + dinero_extra
        self.torre_resaltada = None
        self.imagenes = {}
        self._cargar_imagenes()

        self.frame = tk.Frame(root, bg=COLOR_FONDO)
        self.frame.pack(fill="both", expand=True)
        self._construir_ui()

    def _construir_ui(self):
        tk.Label(
            self.frame,
            text=f"Fase de Construccion - {self.jugador1['nombre']} (Defensor)",
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

        self._construir_tienda()

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
            text="Terminar Construccion",
            font=("Georgia", 12, "bold"),
            bg=COLOR_ACENTO,
            fg=COLOR_FONDO,
            command=self._terminar_construccion,
            padx=15, pady=8
        ).pack(pady=10)

        self._dibujar_mapa()

    def _construir_tienda(self):
        tienda = tk.Frame(self.frame, bg=COLOR_PANEL, padx=10, pady=8)
        tienda.pack(fill="x", padx=20)

        tk.Label(tienda, text="Tienda:", bg=COLOR_PANEL, fg=COLOR_TEXTO, font=("Georgia", 11, "bold")).pack(side="left", padx=5)

        tk.Button(tienda, text="Muro $20", bg="#7f8c8d", fg="white", font=("Georgia", 10),
            command=lambda: self._seleccionar("muro")).pack(side="left", padx=5)
        tk.Button(tienda, text="Torre Basica $50", bg="#3498db", fg="white", font=("Georgia", 10),
            command=lambda: self._seleccionar("torre_basica")).pack(side="left", padx=5)
        tk.Button(tienda, text="Torre Pesada $150", bg="#e67e22", fg="white", font=("Georgia", 10),
            command=lambda: self._seleccionar("torre_pesada")).pack(side="left", padx=5)
        tk.Button(tienda, text="Torre Magica $100", bg="#9b59b6", fg="white", font=("Georgia", 10),
            command=lambda: self._seleccionar("torre_magica")).pack(side="left", padx=5)

        self.label_seleccion = tk.Label(tienda, text="Seleccion: ninguna", bg=COLOR_PANEL, fg=COLOR_ACENTO, font=("Georgia", 10))
        self.label_seleccion.pack(side="left", padx=10)

    def _seleccionar(self, tipo):
        self.seleccion = tipo
        self.label_seleccion.config(text=f"Seleccion: {tipo}")

    def _click_mapa(self, evento):
        col = evento.x // TAMANIO_CASILLA
        fila = evento.y // TAMANIO_CASILLA

        if not self.seleccion:
            messagebox.showwarning("Aviso", "Selecciona un elemento primero.")
            return
        if fila == self.fila_base and col == self.columna_base:
            messagebox.showwarning("Aviso", "No puedes colocar nada sobre la base.")
            return
        if self.mapa[fila][col] is not None:
            messagebox.showwarning("Aviso", "Ya hay algo en esa casilla.")
            return

        if self.seleccion == "muro":
            costo = 20
        elif self.seleccion == "torre_basica":
            costo = 50
        elif self.seleccion == "torre_pesada":
            costo = 150
        elif self.seleccion == "torre_magica":
            costo = 100

        if self.dinero < costo:
            messagebox.showerror("Sin dinero", "No tienes suficiente dinero.")
            return

        if self.seleccion == "muro":
            objeto = Muro()
        elif self.seleccion == "torre_basica":
            objeto = TorreBasica()
        elif self.seleccion == "torre_pesada":
            objeto = TorrePesada()
        elif self.seleccion == "torre_magica":
            objeto = TorreMagica()

        objeto.fila = fila
        objeto.columna = col
        self.mapa[fila][col] = objeto
        self.dinero -= costo
        self.label_dinero.config(text=f"Dinero: {self.dinero}")

        if self.seleccion in ["torre_basica", "torre_pesada", "torre_magica"]:
            self.torre_resaltada = (fila, col, objeto.alcance)
        else:
            self.torre_resaltada = None

        self._dibujar_mapa()

    def _click_derecho(self, evento):
        col = evento.x // TAMANIO_CASILLA
        fila = evento.y // TAMANIO_CASILLA

        if fila == self.fila_base and col == self.columna_base:
            return

        objeto = self.mapa[fila][col]
        if objeto is None:
            return

        if isinstance(objeto, Muro):
            costo = 20
        elif isinstance(objeto, TorreBasica):
            costo = 50
        elif isinstance(objeto, TorrePesada):
            costo = 150
        elif isinstance(objeto, TorreMagica):
            costo = 100
        else:
            costo = 0

        if self.torre_resaltada and self.torre_resaltada[0] == fila and self.torre_resaltada[1] == col:
            self.torre_resaltada = None

        self.mapa[fila][col] = None
        self.dinero += costo
        self.label_dinero.config(text=f"Dinero: {self.dinero}")
        self._dibujar_mapa()

    def _dibujar_mapa(self):
        self.canvas.delete("all")

        casillas_resaltadas = set()
        if self.torre_resaltada:
            fila_t, col_t, alcance = self.torre_resaltada
            for fila in range(FILAS):
                for col in range(COLUMNAS):
                    distancia = abs(fila - fila_t) + abs(col - col_t)
                    if distancia <= alcance:
                        casillas_resaltadas.add((fila, col))

        for fila in range(FILAS):
            for col in range(COLUMNAS):
                x1 = col * TAMANIO_CASILLA
                y1 = fila * TAMANIO_CASILLA
                x2 = x1 + TAMANIO_CASILLA
                y2 = y1 + TAMANIO_CASILLA
                usar_imagen = False
                imagen = None
                texto = ""

                if fila == self.fila_base and col == self.columna_base:
                    texto = "BASE"
                    if "base" in self.imagenes:
                        usar_imagen = True
                        imagen = self.imagenes["base"]
                elif self.mapa[fila][col] is not None:
                    objeto = self.mapa[fila][col]
                    if isinstance(objeto, Muro):
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

                if (fila, col) in casillas_resaltadas:
                    color_fondo = "#2d6b3d"
                else:
                    color_fondo = COLOR_CASILLA

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color_fondo, outline=COLOR_BORDE, width=1)

                if usar_imagen:
                    self.canvas.create_image(x1, y1, anchor="nw", image=imagen)
                elif texto:
                    self.canvas.create_text(x1+25, y1+25, text=texto, fill=COLOR_TEXTO, font=("Georgia", 7, "bold"))

    def _terminar_construccion(self):
        self.frame.destroy()
        self.callback_fin_construccion(self.mapa, self.jugador1, self.jugador2, self.faccion1, self.faccion2, self.vida_base, self.dinero)

    def _cargar_imagenes(self):
        from PIL import Image, ImageTk

        if self.faccion1 == "Reino":
            prefijo = "reino"
        elif self.faccion1 == "Oscura":
            prefijo = "oscura"
        elif self.faccion1 == "Bosque":
            prefijo = "bosque"

        self.imagenes = {}
        tipos = ["muro", "torre_basica", "torre_pesada", "torre_magica", "base"]
        for tipo in tipos:
            ruta = f"assets/imagenes/{prefijo}_{tipo}.png"
            if os.path.exists(ruta):
                img = Image.open(ruta).resize((50, 50), Image.NEAREST)
                self.imagenes[tipo] = ImageTk.PhotoImage(img)