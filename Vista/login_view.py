import tkinter as tk
from tkinter import messagebox
import sys
import os

# Para importar desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sistema_archivos import registrar_jugador, iniciar_sesion

class LoginView:
    def __init__(self, root, callback_login):
        self.root = root
        self.callback_login = callback_login
        self.jugador1 = None
        self.jugador2 = None

        self.frame = tk.Frame(root, bg="#1a1a2e")
        self.frame.pack(fill="both", expand=True)

        self._construir_ui()

    def _construir_ui(self):
        # Título
        tk.Label(
            self.frame,
            text="⚔ Defensa y Asalto de Base ⚔",
            font=("Arial", 22, "bold"),
            bg="#1a1a2e",
            fg="#c9a84c"
        ).pack(pady=30)

        # Panel jugador 1
        self._panel_jugador("Jugador 1", "#16213e", self._login_jugador1, self._registro_jugador1)

        # Panel jugador 2
        self._panel_jugador("Jugador 2", "#0f3460", self._login_jugador2, self._registro_jugador2)

        # Botón iniciar partida
        self.btn_iniciar = tk.Button(
            self.frame,
            text="Iniciar Partida",
            font=("Arial", 14, "bold"),
            bg="#c9a84c",
            fg="#1a1a2e",
            state="disabled",
            command=self._iniciar_partida,
            padx=20,
            pady=10
        )
        self.btn_iniciar.pack(pady=30)

    def _panel_jugador(self, titulo, color, cmd_login, cmd_registro):
        panel = tk.Frame(self.frame, bg=color, padx=20, pady=15)
        panel.pack(pady=10, padx=40, fill="x")

        tk.Label(
            panel,
            text=titulo,
            font=("Arial", 14, "bold"),
            bg=color,
            fg="white"
        ).grid(row=0, column=0, columnspan=2, pady=5)

        tk.Label(panel, text="Usuario:", bg=color, fg="white", font=("Arial", 11)).grid(row=1, column=0, sticky="e", pady=4)
        entry_usuario = tk.Entry(panel, font=("Arial", 11), width=20)
        entry_usuario.grid(row=1, column=1, padx=10, pady=4)

        tk.Label(panel, text="Contraseña:", bg=color, fg="white", font=("Arial", 11)).grid(row=2, column=0, sticky="e", pady=4)
        entry_contra = tk.Entry(panel, font=("Arial", 11), width=20, show="*")
        entry_contra.grid(row=2, column=1, padx=10, pady=4)

        if titulo == "Jugador 1":
            self.label_estado1 = tk.Label(panel, text="Sin iniciar sesión", bg=color, fg="#ff6b6b", font=("Arial", 10))
            self.label_estado1.grid(row=3, column=0, columnspan=2, pady=4)
            self.entry_usuario1 = entry_usuario
            self.entry_contra1 = entry_contra
        else:
            self.label_estado2 = tk.Label(panel, text="Sin iniciar sesión", bg=color, fg="#ff6b6b", font=("Arial", 10))
            self.label_estado2.grid(row=3, column=0, columnspan=2, pady=4)
            self.entry_usuario2 = entry_usuario
            self.entry_contra2 = entry_contra

        frame_botones = tk.Frame(panel, bg=color)
        frame_botones.grid(row=4, column=0, columnspan=2, pady=8)

        tk.Button(
            frame_botones,
            text="Iniciar Sesión",
            font=("Arial", 10),
            bg="#e94560",
            fg="white",
            command=cmd_login,
            padx=10
        ).pack(side="left", padx=5)

        tk.Button(
            frame_botones,
            text="Registrarse",
            font=("Arial", 10),
            bg="#533483",
            fg="white",
            command=cmd_registro,
            padx=10
        ).pack(side="left", padx=5)

    def _login_jugador1(self):
        nombre = self.entry_usuario1.get().strip()
        contra = self.entry_contra1.get().strip()

        if not nombre or not contra:
            messagebox.showwarning("Campos vacíos", "Por favor llena usuario y contraseña.")
            return

        jugador = iniciar_sesion(nombre, contra)
        if jugador:
            self.jugador1 = jugador
            self.label_estado1.config(text=f"✔ {nombre} conectado", fg="#6bff6b")
            self._verificar_ambos_listos()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def _login_jugador2(self):
        nombre = self.entry_usuario2.get().strip()
        contra = self.entry_contra2.get().strip()

        if not nombre or not contra:
            messagebox.showwarning("Campos vacíos", "Por favor llena usuario y contraseña.")
            return

        if self.jugador1 and nombre == self.jugador1["nombre"]:
            messagebox.showerror("Error", "El Jugador 2 no puede ser el mismo que el Jugador 1.")
            return

        jugador = iniciar_sesion(nombre, contra)
        if jugador:
            self.jugador2 = jugador
            self.label_estado2.config(text=f"✔ {nombre} conectado", fg="#6bff6b")
            self._verificar_ambos_listos()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def _registro_jugador1(self):
        nombre = self.entry_usuario1.get().strip()
        contra = self.entry_contra1.get().strip()
        self._registrar(nombre, contra)

    def _registro_jugador2(self):
        nombre = self.entry_usuario2.get().strip()
        contra = self.entry_contra2.get().strip()
        self._registrar(nombre, contra)

    def _registrar(self, nombre, contra):
        if not nombre or not contra:
            messagebox.showwarning("Campos vacíos", "Por favor llena usuario y contraseña.")
            return

        exito = registrar_jugador(nombre, contra)
        if exito:
            messagebox.showinfo("Registro exitoso", f"Jugador '{nombre}' registrado. Ya puedes iniciar sesión.")
        else:
            messagebox.showerror("Error", f"El usuario '{nombre}' ya existe.")

    def _verificar_ambos_listos(self):
        if self.jugador1 and self.jugador2:
            self.btn_iniciar.config(state="normal")

    def _iniciar_partida(self):
        self.frame.destroy()
        self.callback_login(self.jugador1, self.jugador2)