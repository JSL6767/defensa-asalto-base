import tkinter as tk
# Importamos todas las ventanas necesarias
from Vista.login_view import LoginView
from Vista.menu_view import MenuView
from Vista.seleccion_faccion_view import SeleccionFaccionView
from Vista.mapa_view import MapaView

def despues_de_construccion(mapa, jugador1, jugador2, faccion1, faccion2, vida_base):
    # Por ahora solo imprime, aquí irá la fase de ataque
    print("Fase de construcción terminada")
    print(f"Vida de la base: {vida_base}")

def despues_de_facciones(jugador1, jugador2, faccion1, faccion2):
    # Después de elegir facciones abre el mapa para que el defensor construya
    MapaView(root, jugador1, jugador2, faccion1, faccion2, despues_de_construccion)

def despues_del_login(jugador1, jugador2):
    # Después del login abre el menú principal
    MenuView(root, jugador1, jugador2, ir_a_facciones)

def ir_a_facciones(jugador1, jugador2):
    # Desde el menú va a selección de facciones
    SeleccionFaccionView(root, jugador1, jugador2, despues_de_facciones)

def main():
    global root  # global para usarlo en demás funciones
    root = tk.Tk()                              # crea la ventana principal
    root.title("Defensa y Asalto de Base")      # título
    root.geometry("700x800")                    # tamaño
    root.configure(bg="#1a1a2e")                # color de fondo
    root.resizable(False, False)                # no se cambia el tamaño

    LoginView(root, despues_del_login)          # arranca con el login
    root.mainloop()                             # mantiene abierta la ventana

# Solo ejecuta main() si corremos este archivo directamente
if __name__ == "__main__":
    main()