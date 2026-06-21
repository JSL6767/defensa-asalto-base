import tkinter as tk
from tkinter import messagebox
from Vista.login_view import LoginView
from Vista.menu_view import MenuView
from Vista.seleccion_faccion_view import SeleccionFaccionView
from Vista.mapa_view import MapaView
from Vista.ataque_view import AtaqueView
from Vista.combate_view import CombateView
from Vista.fin_ronda_view import FinRondaView
from Vista.fin_partida_view import FinPartidaView
from Vista.fin_dinero_view import FinDineroView

victorias_defensor = 0
victorias_atacante = 0

dinero_extra_defensor_global = 0
dinero_extra_atacante_global = 0

faccion1_global = None
faccion2_global = None

def fin_de_ronda(ganador_ronda, jugador1, jugador2, dinero_defensor_final, dinero_atacante_final):
    global victorias_defensor, victorias_atacante, dinero_extra_defensor_global, dinero_extra_atacante_global

    # Caso especial: el atacante se quedo sin dinero, termina la partida ya
    if ganador_ronda == "sin_dinero":
        FinDineroView(root, jugador1, jugador2, lambda: volver_al_menu(jugador1, jugador2))
        return

    dinero_extra_defensor_global = dinero_defensor_final
    dinero_extra_atacante_global = dinero_atacante_final

    if ganador_ronda == "defensor":
        victorias_defensor += 1
    else:
        victorias_atacante += 1

    if victorias_defensor == 3 or victorias_atacante == 3:
        FinPartidaView(root, ganador_ronda, jugador1, jugador2, victorias_defensor, victorias_atacante, lambda: volver_al_menu(jugador1, jugador2))
    else:
        FinRondaView(root, ganador_ronda, jugador1, jugador2, victorias_defensor, victorias_atacante, lambda: nueva_ronda(jugador1, jugador2))

def nueva_ronda(jugador1, jugador2):
    MapaView(root, jugador1, jugador2, faccion1_global, faccion2_global, despues_de_construccion, dinero_extra_defensor_global)

def volver_al_menu(jugador1, jugador2):
    global victorias_defensor, victorias_atacante, dinero_extra_defensor_global, dinero_extra_atacante_global
    victorias_defensor = 0
    victorias_atacante = 0
    dinero_extra_defensor_global = 0
    dinero_extra_atacante_global = 0
    MenuView(root, jugador1, jugador2, ir_a_facciones)

def despues_del_ataque(mapa, unidades, jugador1, jugador2, faccion1, faccion2, vida_base, dinero_defensor, dinero_atacante):
    CombateView(root, mapa, unidades, jugador1, jugador2, faccion1, faccion2, vida_base, fin_de_ronda, dinero_defensor, dinero_atacante)

def despues_de_construccion(mapa, jugador1, jugador2, faccion1, faccion2, vida_base, dinero_defensor_restante):
    AtaqueView(root, mapa, jugador1, jugador2, faccion1, faccion2, vida_base, despues_del_ataque, dinero_extra_atacante_global, dinero_defensor_restante)

def despues_de_facciones(jugador1, jugador2, faccion1, faccion2):
    global faccion1_global, faccion2_global
    faccion1_global = faccion1
    faccion2_global = faccion2
    MapaView(root, jugador1, jugador2, faccion1, faccion2, despues_de_construccion)

def despues_del_login(jugador1, jugador2):
    MenuView(root, jugador1, jugador2, ir_a_facciones)

def ir_a_facciones(jugador1, jugador2):
    SeleccionFaccionView(root, jugador1, jugador2, despues_de_facciones)

def main():
    global root
    root = tk.Tk()
    root.title("Defensa y Asalto de Base")
    root.geometry("1100x900")
    root.configure(bg="#1a0f1f")
    root.resizable(False, False)

    LoginView(root, despues_del_login)
    root.mainloop()

if __name__ == "__main__":
    main()