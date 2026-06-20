import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Clases.torres import TorreBasica, TorrePesada, TorreMagica
from Clases.muro import Muro
from Clases.unidades import Soldado, Tanque, UnidadRapida

TAMANIO_CASILLA = 45
FILAS = 12
COLUMNAS = 12
FILA_BASE = 5
COLUMNA_BASE = 1

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

class CombateView:
    def __init__(self, root, mapa, unidades, jugador1, jugador2, faccion1, faccion2, vida_base, callback_fin_ronda, dinero_defensor=500, dinero_atacante=500):
        self.root = root
        self.mapa = mapa
        self.unidades = unidades
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.faccion1 = faccion1
        self.faccion2 = faccion2
        self.vida_base = vida_base
        self.callback_fin_ronda = callback_fin_ronda
        self.turno = 0
        self.combate_activo = False

        # El dinero ahora empieza con lo que traían de las fases anteriores
        self.dinero_defensor = dinero_defensor
        self.dinero_atacante = dinero_atacante

        self.imagenes = {}
        self._cargar_imagenes()

        self.frame = tk.Frame(root, bg="#1a1a2e")
        self.frame.pack(fill="both", expand=True)
        self._construir_ui()

    def _construir_ui(self):
        # Título
        tk.Label(
            self.frame,
            text="⚔ Combate ⚔",
            font=("Arial", 16, "bold"),
            bg="#1a1a2e",
            fg="#e74c3c"
        ).pack(pady=10)

        # Vida de la base
        self.label_base = tk.Label(
            self.frame,
            text=f"Vida de la base: {self.vida_base}",
            font=("Arial", 12),
            bg="#1a1a2e",
            fg="white"
        )
        self.label_base.pack()

        # Turno actual
        self.label_turno = tk.Label(
            self.frame,
            text=f"Turno: {self.turno}",
            font=("Arial", 12),
            bg="#1a1a2e",
            fg="#c9a84c"
        )
        self.label_turno.pack()

        # Log de eventos
        self.log = tk.Text(
            self.frame,
            height=3,
            width=60,
            bg="#16213e",
            fg="white",
            font=("Arial", 9),
            state="disabled"
        )
        self.log.pack(pady=5)

        # Canvas del mapa
        self.canvas = tk.Canvas(
            self.frame,
            width=COLUMNAS * TAMANIO_CASILLA,
            height=FILAS * TAMANIO_CASILLA,
            bg="#2d2d44",
            highlightthickness=0
        )
        self.canvas.pack(pady=5)

        # Botón para iniciar el combate
        self.btn_iniciar = tk.Button(
            self.frame,
            text="Iniciar Combate",
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            command=self._iniciar_combate,
            padx=15, pady=8
        )
        self.btn_iniciar.pack(pady=10)

        self._dibujar_mapa()

    def _log(self, mensaje):
        # Agrega un mensaje al log de eventos
        self.log.config(state="normal")
        self.log.insert("end", mensaje + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def _iniciar_combate(self):
        # Desactiva el botón y empieza el combate
        self.btn_iniciar.config(state="disabled")
        self.combate_activo = True
        self._siguiente_turno()

    def _siguiente_turno(self):
        if not self.combate_activo:
            return

        self.turno += 1
        self.label_turno.config(text=f"Turno: {self.turno}")
        self._log(f"--- Turno {self.turno} ---")

        # Fase 1: Torres atacan unidades
        self._torres_atacan()

        # Fase 2: Unidades avanzan y atacan
        self._unidades_avanzan()

        # Redibujamos el mapa
        self._dibujar_mapa()

        # Verificamos si terminó la ronda
        if self._verificar_fin():
            return

        # Siguiente turno después de 800ms
        self.root.after(800, self._siguiente_turno)

    def _torres_atacan(self):
        # Recorremos el mapa buscando torres
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                objeto = self.mapa[fila][col]
                if not isinstance(objeto, (TorreBasica, TorrePesada, TorreMagica)):
                    continue

                # Buscamos unidad en el alcance
                objetivo = self._buscar_objetivo(fila, col, objeto.alcance)
                if objetivo:
                    destruida = objetivo.recibir_daño(objeto.daño)
                    self._log(f"Torre ({fila},{col}) ataca {objetivo.nombre} por {objeto.daño}")

                    # El defensor gana dinero por dañar (poco)
                    self.dinero_defensor += 5
                    self._log(f"Defensor gana $5 por dañar (Total: ${self.dinero_defensor})")

                    # Activamos habilidad especial
                    if isinstance(objeto, TorrePesada):
                        resultado = objeto.habilidad_especial(self.unidades)
                    else:
                        resultado = objeto.habilidad_especial(objetivo)
                    if resultado:
                        self._log(f"Habilidad: {resultado}")

                    if destruida:
                        self._log(f"{objetivo.nombre} eliminado!")
                        self.mapa[objetivo.fila][objetivo.columna] = None
                        self.unidades.remove(objetivo)

                        # El defensor gana MUCHO MÁS dinero por eliminar
                        if isinstance(objetivo, Soldado):
                            ganancia = 40
                        elif isinstance(objetivo, Tanque):
                            ganancia = 100
                        elif isinstance(objetivo, UnidadRapida):
                            ganancia = 60
                        else:
                            ganancia = 30

                        self.dinero_defensor += ganancia
                        self._log(f"Defensor gana ${ganancia} por eliminar (Total: ${self.dinero_defensor})")

    def _buscar_objetivo(self, fila_torre, col_torre, alcance):
        # Busca la unidad más cercana dentro del alcance
        objetivo_cercano = None
        menor_col = COLUMNAS

        for unidad in self.unidades:
            distancia = abs(unidad.fila - fila_torre) + abs(unidad.columna - col_torre)
            if distancia <= alcance and unidad.columna < menor_col:
                objetivo_cercano = unidad
                menor_col = unidad.columna

        return objetivo_cercano

    def _unidades_avanzan(self):
        for unidad in self.unidades[:]:
            fila_actual = unidad.fila
            col_actual = unidad.columna

            if not unidad.mover():
                continue

            col_objetivo = unidad.columna
            unidad.columna = col_actual

            # Si llegó a la base la ataca
            if col_objetivo <= COLUMNA_BASE:
                self.vida_base -= unidad.daño
                self.label_base.config(text=f"Vida de la base: {self.vida_base}")
                self._log(f"{unidad.nombre} ataca BASE por {unidad.daño}!")
                unidad.columna = COLUMNA_BASE

                # El atacante gana dinero por dañar la base
                self.dinero_atacante += 20
                self._log(f"Atacante gana $20 por dañar la base (Total: ${self.dinero_atacante})")
                continue

            objeto_enfrente = self.mapa[fila_actual][col_objetivo]

            if objeto_enfrente is None:
                self.mapa[fila_actual][col_actual] = None
                self.mapa[fila_actual][col_objetivo] = unidad
                unidad.columna = col_objetivo

            elif isinstance(objeto_enfrente, (TorreBasica, TorrePesada, TorreMagica, Muro)):
                destruido = objeto_enfrente.recibir_daño(unidad.daño)
                self._log(f"{unidad.nombre} ataca {objeto_enfrente.nombre} por {unidad.daño}")

                # El atacante gana dinero por dañar una torre/muro
                self.dinero_atacante += 10
                self._log(f"Atacante gana $10 por dañar (Total: ${self.dinero_atacante})")

                if destruido:
                    self._log(f"{objeto_enfrente.nombre} destruido!")
                    self.mapa[fila_actual][col_objetivo] = None

                    # Bonus extra por destruir una torre
                    if not isinstance(objeto_enfrente, Muro):
                        self.dinero_atacante += 30
                        self._log(f"Atacante gana $30 extra por destruir torre (Total: ${self.dinero_atacante})")

                    self.mapa[fila_actual][col_actual] = None
                    self.mapa[fila_actual][col_objetivo] = unidad
                    unidad.columna = col_objetivo
                else:
                    unidad.columna = col_actual

    def _verificar_fin(self):
        if self.vida_base <= 0:
            self.combate_activo = False
            self._log("BASE DESTRUIDA! Gana el atacante!")
            self.frame.destroy()
            self.callback_fin_ronda("atacante", self.jugador1, self.jugador2, self.dinero_defensor, self.dinero_atacante)
            return True

        if not self.unidades:
            self.combate_activo = False
            self._log("Todas las unidades eliminadas! Gana el defensor!")
            self.frame.destroy()
            self.callback_fin_ronda("defensor", self.jugador1, self.jugador2, self.dinero_defensor, self.dinero_atacante)
            return True

        return False

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

                if fila == FILA_BASE and col == COLUMNA_BASE:
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

                # Fondo del mapa
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#2d2d44", outline="#3d3d5c", width=1)

                if usar_imagen:
                    self.canvas.create_image(x1, y1, anchor="nw", image=imagen)
                elif texto:
                    self.canvas.create_text(x1+25, y1+25, text=texto, fill="white", font=("Arial", 7, "bold"))
    
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