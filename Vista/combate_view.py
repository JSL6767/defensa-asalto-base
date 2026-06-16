import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Clases.torres import TorreBasica, TorrePesada, TorreMagica
from Clases.muro import Muro
from Clases.unidades import Soldado, Tanque, UnidadRapida
from sistema_archivos import actualizar_victorias

TAMANIO_CASILLA = 45
FILAS = 12
COLUMNAS = 12
FILA_BASE = 5
COLUMNA_BASE = 1

# Colores para dibujar
COLORES_OBJETOS = {
    Muro:         ("#7f8c8d", "MUR"),
    TorreBasica:  ("#3498db", "TBA"),
    TorrePesada:  ("#e67e22", "TPE"),
    TorreMagica:  ("#9b59b6", "TMA"),
    Soldado:      ("#27ae60", "SOL"),
    Tanque:       ("#c0392b", "TAN"),
    UnidadRapida: ("#f39c12", "RAP"),
}

class CombateView:
    def __init__(self, root, mapa, unidades, jugador1, jugador2, faccion1, faccion2, vida_base, callback_fin_ronda):
        self.root = root
        self.mapa = mapa
        self.unidades = unidades            # lista de unidades del atacante
        self.jugador1 = jugador1            # defensor
        self.jugador2 = jugador2            # atacante
        self.faccion1 = faccion1
        self.faccion2 = faccion2
        self.vida_base = vida_base          # vida de la base central
        self.callback_fin_ronda = callback_fin_ronda
        self.turno = 0                      # contador de turnos
        self.combate_activo = False         # si el combate está corriendo

        self.frame = tk.Frame(root, bg="#1a1a2e")
        self.frame.pack(fill="both", expand=True)
        self._construir_ui()

    def _construir_ui(self):
        # Título
        tk.Label(self.frame, text="⚔ Combate ⚔", font=("Arial", 16, "bold"), bg="#1a1a2e", fg="#e74c3c").pack(pady=10)

        # Info de vida de la base
        self.label_base = tk.Label(self.frame, text=f"Vida de la base: {self.vida_base}", font=("Arial", 12), bg="#1a1a2e", fg="white")
        self.label_base.pack()

        # Info de turno
        self.label_turno = tk.Label(self.frame, text=f"Turno: {self.turno}", font=("Arial", 12), bg="#1a1a2e", fg="#c9a84c")
        self.label_turno.pack()

        # Log de eventos
        self.log = tk.Text(self.frame, height=4, width=60, bg="#16213e", fg="white", font=("Arial", 9), state="disabled")
        self.log.pack(pady=5)

        # Canvas del mapa
        self.canvas = tk.Canvas(self.frame, width=COLUMNAS*TAMANIO_CASILLA, height=FILAS*TAMANIO_CASILLA, bg="#2d2d44", highlightthickness=0)
        self.canvas.pack(pady=5)

        # Botón para iniciar el combate
        self.btn_iniciar = tk.Button(self.frame, text="Iniciar Combate", font=("Arial", 12, "bold"), bg="#e74c3c", fg="white", command=self._iniciar_combate, padx=15, pady=8)
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

        # Fase 1: Torres atacan a las unidades en su alcance
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

                # Buscamos unidades en el alcance de la torre
                objetivo = self._buscar_objetivo(fila, col, objeto.alcance)
                if objetivo:
                    # La torre ataca al objetivo
                    destruida = objetivo.recibir_daño(objeto.daño)
                    self._log(f"Torre en ({fila},{col}) ataca a {objetivo.nombre} por {objeto.daño}")

                    # Activamos habilidad especial si corresponde
                    if isinstance(objeto, TorrePesada):
                        resultado = objeto.habilidad_especial(self.unidades)
                    else:
                        resultado = objeto.habilidad_especial(objetivo)
                    if resultado:
                        self._log(f"Habilidad: {resultado}")

                    if destruida:
                        self._log(f"{objetivo.nombre} fue eliminado!")
                        self.mapa[objetivo.fila][objetivo.columna] = None
                        self.unidades.remove(objetivo)

    def _buscar_objetivo(self, fila_torre, col_torre, alcance):
        # Busca la unidad mas cercana dentro del alcance
        objetivo_cercano = None
        menor_col = COLUMNAS

        for unidad in self.unidades:
            distancia = abs(unidad.fila - fila_torre) + abs(unidad.columna - col_torre)
            if distancia <= alcance and unidad.columna < menor_col:
                objetivo_cercano = unidad
                menor_col = unidad.columna

        return objetivo_cercano

    def _unidades_avanzan(self):
        # Cada unidad avanza hacia la base
        for unidad in self.unidades[:]:
            col_anterior = unidad.columna

            # Intentamos mover la unidad
            if not unidad.mover():
                continue  # estaba congelada

            nueva_col = unidad.columna

            # Verificamos si llegó a la base
            if unidad.fila == FILA_BASE and unidad.columna <= COLUMNA_BASE:
                self.vida_base -= unidad.daño
                self.label_base.config(text=f"Vida de la base: {self.vida_base}")
                self._log(f"{unidad.nombre} ataca la BASE por {unidad.daño}! Vida restante: {self.vida_base}")
                # La unidad se queda en la base
                unidad.columna = COLUMNA_BASE
            else:
                # Verificamos si chocó con un muro o torre
                if self.mapa[unidad.fila][nueva_col] is not None and not isinstance(self.mapa[unidad.fila][nueva_col], type(unidad)):
                    objeto = self.mapa[unidad.fila][nueva_col]
                    destruido = objeto.recibir_daño(unidad.daño)
                    self._log(f"{unidad.nombre} ataca {objeto.nombre} por {unidad.daño}")
                    if destruido:
                        self._log(f"{objeto.nombre} fue destruido!")
                        self.mapa[unidad.fila][nueva_col] = None
                    unidad.columna = col_anterior  # no avanza si hay obstaculo
                else:
                    # Actualiza posición en el mapa
                    self.mapa[unidad.fila][col_anterior] = None
                    self.mapa[unidad.fila][nueva_col] = unidad

    def _verificar_fin(self):
        # El atacante gana si destruye la base
        if self.vida_base <= 0:
            self.combate_activo = False
            self._log("LA BASE FUE DESTRUIDA! Gana el atacante!")
            messagebox.showinfo("Fin de ronda", f"¡{self.jugador2['nombre']} gana la ronda!")
            actualizar_victorias(self.jugador2["nombre"], "atacante")
            self.frame.destroy()
            self.callback_fin_ronda("atacante", self.jugador1, self.jugador2)
            return True

        # El defensor gana si no quedan unidades
        if not self.unidades:
            self.combate_activo = False
            self._log("Todas las unidades fueron eliminadas! Gana el defensor!")
            messagebox.showinfo("Fin de ronda", f"¡{self.jugador1['nombre']} gana la ronda!")
            actualizar_victorias(self.jugador1["nombre"], "defensor")
            self.frame.destroy()
            self.callback_fin_ronda("defensor", self.jugador1, self.jugador2)
            return True

        return False

    def _dibujar_mapa(self):
        self.canvas.delete("all")
        for fila in range(FILAS):
            for col in range(COLUMNAS):
                x1, y1 = col * TAMANIO_CASILLA, fila * TAMANIO_CASILLA
                x2, y2 = x1 + TAMANIO_CASILLA, y1 + TAMANIO_CASILLA
                objeto = self.mapa[fila][col]

                if fila == FILA_BASE and col == COLUMNA_BASE:
                    color, texto = "#e74c3c", "BASE"
                elif objeto is None:
                    color, texto = "#2d2d44", ""
                else:
                    color, texto = COLORES_OBJETOS.get(type(objeto), ("#2d2d44", ""))

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#1a1a2e", width=1)
                if texto:
                    self.canvas.create_text(x1+25, y1+25, text=texto, fill="white", font=("Arial", 7, "bold"))