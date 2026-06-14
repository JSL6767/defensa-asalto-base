import tkinter as tk
from Vista.login_view import LoginView

def iniciar_juego(jugador1, jugador2):
    print(f"Partida iniciada: {jugador1['nombre']} vs {jugador2['nombre']}")

def main():
    root = tk.Tk()
    root.title("Defensa y Asalto de Base")
    root.geometry("700x600")
    root.configure(bg="#1a1a2e")
    root.resizable(False, False)

    LoginView(root, iniciar_juego)
    root.mainloop()

if __name__ == "__main__":
    main()