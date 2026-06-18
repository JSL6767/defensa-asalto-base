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
    def __init__(self, root, mapa, unidades, jugador1, jugador2, faccion1, faccion2, vida_base, callback_fin_ronda):
        self.root = root
        self.mapa = mapa
        self.unidades = unidades            # lista de unidades del atacante
        self.jugador1 = jugador1            # defensor
        self.jugador2 = jugador2            # atacante
        self.faccion1 = faccion1            # facción del defensor
        self.faccion2 = faccion2            # facción del atacante
        self.vida_base = vida_base          # vida de la base central
        self.callback_fin_ronda = callback_fin_ronda
        self.turno = 0                      # contador de turnos
        self.combate_activo = False         # si el combate está corriendo
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
            col_anterior = unidad.columna

            if not unidad.mover():
                continue  # estaba congelada

            nueva_col = unidad.columna

            # Si llegó a la columna de la base ataca
            if nueva_col <= COLUMNA_BASE:
                self.vida_base -= unidad.daño
                self.label_base.config(text=f"Vida de la base: {self.vida_base}")
                self._log(f"{unidad.nombre} ataca BASE por {unidad.daño}! Vida: {self.vida_base}")
                unidad.columna = COLUMNA_BASE
            else:
                # Verificamos si chocó con algo
                if self.mapa[unidad.fila][nueva_col] is not None and not isinstance(self.mapa[unidad.fila][nueva_col], type(unidad)):
                    objeto = self.mapa[unidad.fila][nueva_col]
                    destruido = objeto.recibir_daño(unidad.daño)
                    self._log(f"{unidad.nombre} ataca {objeto.nombre} por {unidad.daño}")
                    if destruido:
                        self._log(f"{objeto.nombre} destruido!")
                        self.mapa[unidad.fila][nueva_col] = None
                    unidad.columna = col_anterior  # no avanza si hay obstáculo
                else:
                    # Actualiza posición en el mapa
                    self.mapa[unidad.fila][col_anterior] = None
                    self.mapa[unidad.fila][nueva_col] = unidad

    def _verificar_fin(self):
        # El atacante gana si destruye la base
        if self.vida_base <= 0:
            self.combate_activo = False
            self._log("BASE DESTRUIDA! Gana el atacante!")
            self.frame.destroy()
            self.callback_fin_ronda("atacante", self.jugador1, self.jugador2)
            return True

        # El defensor gana si no quedan unidades
        if not self.unidades:
            self.combate_activo = False
            self._log("Todas las unidades eliminadas! Gana el defensor!")
            self.frame.destroy()
            self.callback_fin_ronda("defensor", self.jugador1, self.jugador2)
            return True

        return False

    def _dibujar_mapa(self):
        self.canvas.delete("all")

        # Colores según facción del defensor
        color_torre, color_muro, color_base = obtener_colores_faccion(self.faccion1)

        # Color de unidades según facción del atacante
        if self.faccion2 == "Reino":
            color_unidad = "#c9a84c"
        elif self.faccion2 == "Oscura":
            color_unidad = "#7b2d8b"
        elif self.faccion2 == "Bosque":
            color_unidad = "#2d8b3b"
        else:
            color_unidad = "#27ae60"

        for fila in range(FILAS):
            for col in range(COLUMNAS):
                x1 = col * TAMANIO_CASILLA
                y1 = fila * TAMANIO_CASILLA
                x2 = x1 + TAMANIO_CASILLA
                y2 = y1 + TAMANIO_CASILLA
                objeto = self.mapa[fila][col]
                usar_imagen = False

                if fila == FILA_BASE and col == COLUMNA_BASE:
                    color = color_base
                    texto = "BASE"
                elif objeto is None:
                    color = "#2d2d44"
                    texto = ""
                elif isinstance(objeto, Muro):
                    color = color_muro
                    texto = "MUR"
                elif isinstance(objeto, TorreBasica):
                    color = color_torre
                    texto = "TBA"
                elif isinstance(objeto, TorrePesada):
                    color = color_torre
                    texto = "TPE"
                elif isinstance(objeto, TorreMagica):
                    color = color_torre
                    texto = "TMA"
                elif isinstance(objeto, Soldado):
                    color = color_unidad
                    texto = "SOL"
                    if "soldado" in self.imagenes:
                        usar_imagen = True
                        imagen = self.imagenes["soldado"]
                elif isinstance(objeto, Tanque):
                    color = color_unidad
                    texto = "TAN"
                    if "tanque" in self.imagenes:
                        usar_imagen = True
                        imagen = self.imagenes["tanque"]
                elif isinstance(objeto, UnidadRapida):
                    color = color_unidad
                    texto = "RAP"
                    if "rapida" in self.imagenes:
                        usar_imagen = True
                        imagen = self.imagenes["rapida"]
                else:
                    color = "#2d2d44"
                    texto = ""

                # Dibuja el rectángulo de fondo siempre
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#1a1a2e", width=1)

                # Si hay imagen la dibuja, si no dibuja el texto
                if usar_imagen:
                    self.canvas.create_image(x1, y1, anchor="nw", image=imagen)
                elif texto:
                    self.canvas.create_text(x1+25, y1+25, text=texto, fill="white", font=("Arial", 7, "bold"))

    def _cargar_imagenes(self):
        from PIL import Image, ImageTk
        import os

        if self.faccion2 == "Reino":
            prefijo = "reino"
        elif self.faccion2 == "Oscura":
            prefijo = "oscura"
        elif self.faccion2 == "Bosque":
            prefijo = "bosque"

        tipos = ["soldado", "tanque", "rapida"]
        for tipo in tipos:
            ruta = f"assets/imagenes/{prefijo}_{tipo}.png"
            if os.path.exists(ruta):
                img = Image.open(ruta).resize((45, 45), Image.LANCZOS)
                self.imagenes[tipo] = ImageTk.PhotoImage(img)