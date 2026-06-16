import tkinter as tk
#Importamos ventanas creadas
from Vista.login_view import LoginView
from Vista.menu_view import MenuView
from Vista.seleccion_faccion_view import SeleccionFaccionView

def despues_de_facciones(jugador1, jugador2, faccion1, faccion2):
    #La funcion se ejecuta cuando ambos jugadores eligen facción
    #Por ahora imprime, despues irá el mapa
    print(f"{jugador1['nombre']} eligió {faccion1}")
    print(f"{jugador2['nombre']} eligió {faccion2}")

def despues_del_login(jugador1, jugador2):
    #Se ejecuta cuando los jugadores inician sesión correctamente
    # Después del login abre la ventana de selección de facciones
    MenuView(root, jugador1, jugador2, ir_a_facciones)

def ir_a_facciones(jugador1, jugador2):
    SeleccionFaccionView(root, jugador1, jugador2, despues_de_facciones)

def main():
    global root #global para usarlo en demás funciones
    root = tk.Tk()  #crea ventana principal
    root.title("Defensa y Asalto de Base")  #título 
    root.geometry("700x800")  #tamaño
    root.configure(bg="#1a1a2e") #color de fondo
    root.resizable(False, False)  #no se cambia el tamaño

    LoginView(root, despues_del_login) #abre el login, le pasa la ventana y el callback
    root.mainloop() #mantiene abierta la ventana

if __name__ == "__main__":   #solo ejecuta main() 
    main()