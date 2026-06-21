import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Clases.torres import TorreBasica, TorrePesada, TorreMagica
from Clases.muro import Muro
from Clases.unidades import Soldado, Tanque, UnidadRapida

TAMANIO_CASILLA = 50
FILAS = 12
COLUMNAS = 12
FILA_BASE = 5
COLUMNA_BASE = 1

COLOR_FONDO = "#1a0f1f"
COLOR_PANEL = "#3d1530"
COLOR_CASILLA = "#3d1530"
COLOR_BORDE = "#5e1f3d"
COLOR_ACENTO = "#9b4f7f"
COLOR_TEXTO = "#e8d5e0"

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

        self.dinero_defensor = dinero_defensor
        self.dinero_atacante = dinero_atacante

        self.cooldown_torre_basica = 0
        self.cooldown_torre_pesada = 0
        self.cooldown_torre_magica = 0
        self.cooldown_soldado = 0
        self.cooldown_tanque = 0
        self.cooldown_rapida = 0
        self.COOLDOWN_MAX = 5

        self.imagenes = {}
        self._cargar_imagenes()

        self.frame = tk.Frame(root, bg=COLOR_FONDO)
        self.frame.pack(fill="both", expand=True)
        self._construir_ui()

    def _construir_ui(self):
        tk.Label(self.frame, text="Combate", font=("Georgia", 16, "bold"), bg=COLOR_FONDO, fg=COLOR_ACENTO).pack(pady=10)

        contenedor = tk.Frame(self.frame, bg=COLOR_FONDO)
        contenedor.pack(pady=5)

        columna_mapa = tk.Frame(contenedor, bg=COLOR_FONDO)
        columna_mapa.pack(side="left", padx=10)

        self.canvas = tk.Canvas(columna_mapa, width=COLUMNAS*TAMANIO_CASILLA, height=FILAS*TAMANIO_CASILLA, bg=COLOR_FONDO, highlightthickness=0)
        self.canvas.pack()

        columna_controles = tk.Frame(contenedor, bg=COLOR_FONDO, width=200)
        columna_controles.pack(side="left", padx=10, fill="y")

        self.label_base = tk.Label(columna_controles, text=f"Vida de la base: {self.vida_base}", font=("Georgia", 12), bg=COLOR_FONDO, fg=COLOR_TEXTO, wraplength=200)
        self.label_base.pack(pady=10)

        self.label_turno = tk.Label(columna_controles, text=f"Turno: {self.turno}", font=("Georgia", 12), bg=COLOR_FONDO, fg=COLOR_ACENTO)
        self.label_turno.pack(pady=5)

        self.log = tk.Text(columna_controles, height=15, width=28, bg=COLOR_PANEL, fg=COLOR_TEXTO, font=("Georgia", 9), state="disabled", wrap="word")
        self.log.pack(pady=10)

        self.btn_iniciar = tk.Button(
            columna_controles, text="Iniciar Combate", font=("Georgia", 12, "bold"),
            bg=COLOR_ACENTO, fg=COLOR_FONDO, command=self._iniciar_combate, padx=15, pady=8
        )
        self.btn_iniciar.pack(pady=10)

        self.root.bind("<KeyPress>", self._tecla_presionada)
        self.root.focus_set()

        self._dibujar_mapa()

    def _log(self, mensaje):
        self.log.config(state="normal")
        self.log.insert("end", mensaje + "\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def _tecla_presionada(self, evento):
        tecla = evento.char.lower()

        if tecla == "a":
            self._activar_habilidad_torre(TorreBasica, "cooldown_torre_basica", "Torre Basica")
        elif tecla == "s":
            self._activar_habilidad_torre(TorrePesada, "cooldown_torre_pesada", "Torre Pesada")
        elif tecla == "d":
            self._activar_habilidad_torre(TorreMagica, "cooldown_torre_magica", "Torre Magica")
        elif tecla == "j":
            self._activar_habilidad_unidad(Soldado, "cooldown_soldado", "Soldado")
        elif tecla == "k":
            self._activar_habilidad_unidad(Tanque, "cooldown_tanque", "Tanque")
        elif tecla == "l":
            self._activar_habilidad_unidad(UnidadRapida, "cooldown_rapida", "Unidad Rapida")

    def _activar_habilidad_torre(self, clase_torre, atributo_cooldown, nombre):
        if getattr(self, atributo_cooldown) > 0:
            self._log(f"{nombre} en espera ({getattr(self, atributo_cooldown)} turnos)")
            return

        activada = False
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                objeto = self.mapa[fila][col]
                if isinstance(objeto, clase_torre):
                    objetivo = self._buscar_objetivo(fila, col, objeto.alcance)
                    if objetivo:
                        if clase_torre == TorrePesada:
                            resultado = objeto.habilidad_especial(self.unidades)
                        else:
                            resultado = objeto.habilidad_especial(objetivo)
                        if resultado:
                            self._log(f"[{nombre}] {resultado}")
                            self._parpadear_objeto(fila, col)
                            activada = True

        if activada:
            setattr(self, atributo_cooldown, self.COOLDOWN_MAX)
            self._log(f"{nombre}: habilidad activada")
        else:
            self._log(f"{nombre}: no hay objetivos en alcance")

    def _activar_habilidad_unidad(self, clase_unidad, atributo_cooldown, nombre):
        if getattr(self, atributo_cooldown) > 0:
            self._log(f"{nombre} en espera ({getattr(self, atributo_cooldown)} turnos)")
            return

        activada = False
        for unidad in self.unidades:
            if isinstance(unidad, clase_unidad):
                if isinstance(unidad, Soldado):
                    col_enfrente = unidad.columna - 1
                    if col_enfrente >= 0:
                        objetivo = self.mapa[unidad.fila][col_enfrente]
                    else:
                        objetivo = None
                    resultado = unidad.habilidad_especial(objetivo)
                else:
                    resultado = unidad.habilidad_especial(None)

                if resultado:
                    self._log(f"[{nombre}] {resultado}")
                    self._parpadear_objeto(unidad.fila, unidad.columna)
                    activada = True

        if activada:
            setattr(self, atributo_cooldown, self.COOLDOWN_MAX)
            self._log(f"{nombre}: habilidad activada")
        else:
            self._log(f"{nombre}: sin objetivo o no hay unidades de este tipo")

    def _parpadear_objeto(self, fila, col):
        x1 = col * TAMANIO_CASILLA
        y1 = fila * TAMANIO_CASILLA
        x2 = x1 + TAMANIO_CASILLA
        y2 = y1 + TAMANIO_CASILLA

        destello = self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="#c9596f", outline="#e8a8b8", width=3)
        self.canvas.tag_raise(destello)
        self.root.after(600, lambda: self.canvas.delete(destello))

    def _iniciar_combate(self):
        self.btn_iniciar.config(state="disabled")
        self.combate_activo = True
        self._siguiente_turno()

    def _siguiente_turno(self):
        if not self.combate_activo:
            return

        self.root.focus_set()
        self.turno += 1
        self.label_turno.config(text=f"Turno: {self.turno}")

        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

        self._log(f"--- Turno {self.turno} ---")

        if self.cooldown_torre_basica > 0:
            self.cooldown_torre_basica -= 1
        if self.cooldown_torre_pesada > 0:
            self.cooldown_torre_pesada -= 1
        if self.cooldown_torre_magica > 0:
            self.cooldown_torre_magica -= 1
        if self.cooldown_soldado > 0:
            self.cooldown_soldado -= 1
        if self.cooldown_tanque > 0:
            self.cooldown_tanque -= 1
        if self.cooldown_rapida > 0:
            self.cooldown_rapida -= 1

        self._torres_atacan()
        self._unidades_avanzan()
        self._dibujar_mapa()

        if self._verificar_fin():
            return

        self.root.after(1500, self._siguiente_turno)

    def _torres_atacan(self):
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                objeto = self.mapa[fila][col]
                if not isinstance(objeto, (TorreBasica, TorrePesada, TorreMagica)):
                    continue

                objetivo = self._buscar_objetivo(fila, col, objeto.alcance)
                if objetivo:
                    fila_objetivo = objetivo.fila
                    col_objetivo = objetivo.columna

                    destruida = objetivo.recibir_daño(objeto.daño)
                    self._log(f"Torre ({fila},{col}) ataca {objetivo.nombre} por {objeto.daño}")

                    if destruida:
                        self._log(f"{objetivo.nombre} eliminado")
                        self.mapa[fila_objetivo][col_objetivo] = None
                        if objetivo in self.unidades:
                            self.unidades.remove(objetivo)

                        if isinstance(objetivo, Soldado):
                            ganancia = 40
                        elif isinstance(objetivo, Tanque):
                            ganancia = 100
                        elif isinstance(objetivo, UnidadRapida):
                            ganancia = 60
                        else:
                            ganancia = 30

                        self.dinero_defensor += ganancia
                        self._log(f"Defensor gana ${ganancia} (Total: ${self.dinero_defensor})")

    def _buscar_objetivo(self, fila_torre, col_torre, alcance):
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

            if col_objetivo <= COLUMNA_BASE:
                unidad_en_base = any(u.fila == fila_actual and u.columna == COLUMNA_BASE for u in self.unidades if u is not unidad)
                if unidad_en_base:
                    unidad.columna = col_actual
                    continue

                self.vida_base -= unidad.daño
                self.label_base.config(text=f"Vida de la base: {self.vida_base}")
                self._log(f"{unidad.nombre} ataca BASE por {unidad.daño}")
                unidad.columna = COLUMNA_BASE
                continue

            objeto_enfrente = self.mapa[fila_actual][col_objetivo]

            if objeto_enfrente is None:
                unidad.columna = col_objetivo

            elif isinstance(objeto_enfrente, (Soldado, Tanque, UnidadRapida)):
                unidad.columna = col_actual

            elif isinstance(objeto_enfrente, (TorreBasica, TorrePesada, TorreMagica, Muro)):
                destruido = objeto_enfrente.recibir_daño(unidad.daño)
                self._log(f"{unidad.nombre} ataca {objeto_enfrente.nombre} por {unidad.daño}")

                if destruido:
                    self._log(f"{objeto_enfrente.nombre} destruido")
                    self.mapa[fila_actual][col_objetivo] = None

                    if isinstance(objeto_enfrente, TorreBasica):
                        bonus = 20
                    elif isinstance(objeto_enfrente, TorrePesada):
                        bonus = 50
                    elif isinstance(objeto_enfrente, TorreMagica):
                        bonus = 40
                    elif isinstance(objeto_enfrente, Muro):
                        bonus = 5
                    else:
                        bonus = 0

                    self.dinero_atacante += bonus
                    self._log(f"Atacante gana ${bonus} extra por destruir (Total: ${self.dinero_atacante})")
                    unidad.columna = col_objetivo
                else:
                    unidad.columna = col_actual
            else:
                unidad.columna = col_actual

        for fila in range(FILAS):
            for col in range(COLUMNAS):
                objeto_actual = self.mapa[fila][col]
                if isinstance(objeto_actual, (Soldado, Tanque, UnidadRapida)):
                    self.mapa[fila][col] = None

        for unidad in self.unidades:
            if unidad.columna == COLUMNA_BASE:
                continue
            self.mapa[unidad.fila][unidad.columna] = unidad

    def _verificar_fin(self):
        if self.vida_base <= 0:
            self.combate_activo = False
            self._log("BASE DESTRUIDA - Gana el atacante")
            self.dinero_atacante += 100
            self._log(f"Atacante gana $100 por destruir la base (Total: ${self.dinero_atacante})")
            self.frame.destroy()
            self.callback_fin_ronda("atacante", self.jugador1, self.jugador2, self.dinero_defensor, self.dinero_atacante)
            return True

        if not self.unidades:
            self.combate_activo = False
            self._log("Todas las unidades eliminadas - Gana el defensor")

            # Si el atacante se quedo sin dinero suficiente para seguir
            # comprando unidades, termina la partida completa de inmediato
            if self.dinero_atacante < 30:
                self._log("El atacante se quedo sin dinero suficiente!")
                self.frame.destroy()
                self.callback_fin_ronda("sin_dinero", self.jugador1, self.jugador2, self.dinero_defensor, self.dinero_atacante)
                return True

            self.frame.destroy()
            self.callback_fin_ronda("defensor", self.jugador1, self.jugador2, self.dinero_defensor, self.dinero_atacante)
            return True

        return False

    def _dibujar_mapa(self):
        self.canvas.delete("all")

        fila_atacando_base = None
        unidad_en_base = None
        for unidad in self.unidades:
            if unidad.columna == COLUMNA_BASE:
                fila_atacando_base = unidad.fila
                unidad_en_base = unidad
                break

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
                elif fila == fila_atacando_base and col == COLUMNA_BASE + 1 and self.mapa[fila][col] is None:
                    if isinstance(unidad_en_base, Soldado):
                        texto = "SOL"
                        if "soldado" in self.imagenes:
                            usar_imagen = True
                            imagen = self.imagenes["soldado"]
                    elif isinstance(unidad_en_base, Tanque):
                        texto = "TAN"
                        if "tanque" in self.imagenes:
                            usar_imagen = True
                            imagen = self.imagenes["tanque"]
                    elif isinstance(unidad_en_base, UnidadRapida):
                        texto = "RAP"
                        if "rapida" in self.imagenes:
                            usar_imagen = True
                            imagen = self.imagenes["rapida"]
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

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_CASILLA, outline=COLOR_BORDE, width=1)

                if usar_imagen:
                    self.canvas.create_image(x1, y1, anchor="nw", image=imagen)
                elif texto:
                    self.canvas.create_text(x1+25, y1+25, text=texto, fill=COLOR_TEXTO, font=("Georgia", 7, "bold"))

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