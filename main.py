import tkinter as tk
from tkinter import messagebox
# Importamos todas las ventanas
from Vista.login_view import LoginView
from Vista.menu_view import MenuView
from Vista.seleccion_faccion_view import SeleccionFaccionView
from Vista.mapa_view import MapaView
from Vista.ataque_view import AtaqueView
from Vista.combate_view import CombateView
from Vista.fin_ronda_view import FinRondaView
from Vista.fin_partida_view import FinPartidaView

# Contador de victorias por ronda
victorias_defensor = 0
victorias_atacante = 0

faccion1_global = None  # facción del defensor guardada
faccion2_global = None  # facción del atacante guardada

def fin_de_ronda(ganador_ronda, jugador1, jugador2):
    global victorias_defensor, victorias_atacante

    # Sumamos la victoria según quien ganó
    if ganador_ronda == "defensor":
        victorias_defensor += 1
    else:
        victorias_atacante += 1

    # Verificamos si alguien ganó la partida completa
    if victorias_defensor == 3 or victorias_atacante == 3:
        # Alguien ganó la partida
        FinPartidaView(root, ganador_ronda, jugador1, jugador2, victorias_defensor, victorias_atacante, lambda: volver_al_menu(jugador1, jugador2))
    else:
        # Nadie ha ganado aún, mostramos el marcador y continuamos
        FinRondaView(root, ganador_ronda, jugador1, jugador2, victorias_defensor, victorias_atacante, lambda: nueva_ronda(jugador1, jugador2))

def nueva_ronda(jugador1, jugador2):
    # Usa las facciones ya elegidas, no vuelve a preguntar
    MapaView(root, jugador1, jugador2, faccion1_global, faccion2_global, despues_de_construccion)

def volver_al_menu(jugador1, jugador2):
    global victorias_defensor, victorias_atacante
    # Reiniciamos el conteo y volvemos al menú  
    victorias_defensor = 0
    victorias_atacante = 0
    MenuView(root, jugador1, jugador2, ir_a_facciones)

def despues_del_ataque(mapa, unidades, jugador1, jugador2, faccion1, faccion2, vida_base):
    # Después del ataque inicia el combate
    CombateView(root, mapa, unidades, jugador1, jugador2, faccion1, faccion2, vida_base, fin_de_ronda)

def despues_de_construccion(mapa, jugador1, jugador2, faccion1, faccion2, vida_base):
    # Después de construir abre la fase de ataque
    AtaqueView(root, mapa, jugador1, jugador2, faccion1, faccion2, vida_base, despues_del_ataque)

def despues_de_facciones(jugador1, jugador2, faccion1, faccion2):
    global faccion1_global, faccion2_global
    # Guardamos las facciones para usarlas en rondas siguientes
    faccion1_global = faccion1
    faccion2_global = faccion2
    MapaView(root, jugador1, jugador2, faccion1, faccion2, despues_de_construccion)

def despues_del_login(jugador1, jugador2):
    # Después del login abre el menú principal
    MenuView(root, jugador1, jugador2, ir_a_facciones)

def ir_a_facciones(jugador1, jugador2):
    # Desde el menú va a selección de facciones
    SeleccionFaccionView(root, jugador1, jugador2, despues_de_facciones)

def main():
    global root
    root = tk.Tk()
    root.title("Defensa y Asalto de Base")
    root.geometry("800x950")                    # tamaño de la ventana
    root.configure(bg="#1a1a2e")                # color de fondo
    root.resizable(False, False)                # no se cambia el tamaño

    LoginView(root, despues_del_login)          # arranca con el login
    root.mainloop()                             # mantiene abierta la ventana

# Solo ejecuta main() si corremos este archivo directamente
if __name__ == "__main__":
    main()