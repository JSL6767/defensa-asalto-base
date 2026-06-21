import tkinter as tk
from tkinter import messagebox
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sistema_archivos import registrar_jugador, iniciar_sesion

COLOR_FONDO = "#1a0f1f"
COLOR_TARJETA = "#2a1320"
COLOR_BORDE = "#5e1f3d"
COLOR_AVATAR = "#5e1f3d"
COLOR_BOTON_PRINCIPAL = "#7b1e3a"
COLOR_BOTON_SECUNDARIO = "#9b4f7f"
COLOR_ACENTO = "#9b4f7f"
COLOR_ROSADO = "#c9596f"
COLOR_TEXTO = "#e8d5e0"
COLOR_TEXTO_SEC = "#c9a8bb"
COLOR_ERROR = "#c97b7b"
COLOR_EXITO = "#a8c97b"

class LoginView:
    def __init__(self, root, callback_login):
        self.root = root
        self.callback_login = callback_login
        self.jugador1 = None
        self.jugador2 = None

        self.frame = tk.Frame(root, bg=COLOR_FONDO)
        self.frame.pack(fill="both", expand=True)

        self._construir_pantalla(1)

    def _construir_pantalla(self, numero):
        for widget in self.frame.winfo_children():
            widget.destroy()

        rol = "Defensor" if numero == 1 else "Atacante"

        # Encabezado
        tk.Label(
            self.frame, text="DEFENSA Y ASALTO DE BASE",
            font=("Georgia", 11), bg=COLOR_FONDO, fg=COLOR_ACENTO
        ).pack(pady=(50, 4))

        tk.Label(
            self.frame, text="Inicio de sesion",
            font=("Georgia", 22), bg=COLOR_FONDO, fg=COLOR_TEXTO
        ).pack(pady=(0, 4))

        tk.Label(
            self.frame, text=f"Paso {numero} de 2  -  {rol}",
            font=("Georgia", 11), bg=COLOR_FONDO, fg=COLOR_ROSADO
        ).pack(pady=(0, 30))

        # Tarjeta central
        tarjeta = tk.Frame(self.frame, bg=COLOR_TARJETA, highlightbackground=COLOR_BORDE, highlightthickness=1, padx=30, pady=25)
        tarjeta.pack()

        # Avatar numerado
        avatar = tk.Frame(tarjeta, bg=COLOR_AVATAR, width=64, height=64)
        avatar.pack(pady=(0, 16))
        avatar.pack_propagate(False)
        tk.Label(avatar, text=str(numero), font=("Georgia", 18, "bold"), bg=COLOR_AVATAR, fg=COLOR_TEXTO).pack(expand=True)

        # Campo usuario
        tk.Label(tarjeta, text="Usuario", font=("Georgia", 10), bg=COLOR_TARJETA, fg=COLOR_TEXTO_SEC, anchor="w").pack(fill="x")
        entry_usuario = tk.Entry(tarjeta, font=("Georgia", 11), bg=COLOR_FONDO, fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
                                   relief="solid", bd=1, highlightbackground=COLOR_BORDE, highlightcolor=COLOR_ACENTO, width=28)
        entry_usuario.pack(pady=(4, 14), ipady=5)

        # Campo contraseña
        tk.Label(tarjeta, text="Contrasena", font=("Georgia", 10), bg=COLOR_TARJETA, fg=COLOR_TEXTO_SEC, anchor="w").pack(fill="x")
        entry_contra = tk.Entry(tarjeta, font=("Georgia", 11), bg=COLOR_FONDO, fg=COLOR_TEXTO, insertbackground=COLOR_TEXTO,
                                  relief="solid", bd=1, highlightbackground=COLOR_BORDE, highlightcolor=COLOR_ACENTO, width=28, show="*")
        entry_contra.pack(pady=(4, 14), ipady=5)

        # Estado de la sesión
        label_estado = tk.Label(tarjeta, text="Sin iniciar sesion", font=("Georgia", 10), bg=COLOR_TARJETA, fg=COLOR_ERROR)
        label_estado.pack(pady=(0, 14))

        # Botones de acción
        frame_botones = tk.Frame(tarjeta, bg=COLOR_TARJETA)
        frame_botones.pack(fill="x")

        btn_login = tk.Button(
            frame_botones, text="Iniciar sesion", font=("Georgia", 10),
            bg=COLOR_BOTON_PRINCIPAL, fg=COLOR_TEXTO, relief="flat",
            activebackground=COLOR_BOTON_PRINCIPAL, activeforeground=COLOR_TEXTO,
            command=lambda: self._login(numero, entry_usuario, entry_contra, label_estado)
        )
        btn_login.pack(side="left", expand=True, fill="x", ipady=8, padx=(0, 5))

        btn_registro = tk.Button(
            frame_botones, text="Registrarse", font=("Georgia", 10),
            bg=COLOR_TARJETA, fg=COLOR_ACENTO, relief="solid", bd=1,
            activebackground=COLOR_TARJETA, activeforeground=COLOR_ACENTO,
            highlightbackground=COLOR_ACENTO,
            command=lambda: self._registrar(entry_usuario, entry_contra)
        )
        btn_registro.pack(side="left", expand=True, fill="x", ipady=8, padx=(5, 0))

        # Botón continuar/iniciar partida
        texto_boton = "Continuar" if numero == 1 else "Iniciar Partida"
        comando = (lambda: self._construir_pantalla(2)) if numero == 1 else self._iniciar_partida

        self.btn_avanzar = tk.Button(
            self.frame, text=texto_boton, font=("Georgia", 12, "bold"),
            bg=COLOR_ACENTO, fg=COLOR_FONDO, relief="flat",
            activebackground=COLOR_ACENTO, activeforeground=COLOR_FONDO,
            state="disabled", command=comando, padx=36, pady=10
        )
        self.btn_avanzar.pack(pady=30)

        # Guardamos referencias según el paso
        if numero == 1:
            self.entry_usuario1 = entry_usuario
            self.entry_contra1 = entry_contra
            self.label_estado1 = label_estado
        else:
            self.entry_usuario2 = entry_usuario
            self.entry_contra2 = entry_contra
            self.label_estado2 = label_estado

    def _login(self, numero, entry_usuario, entry_contra, label_estado):
        nombre = entry_usuario.get().strip()
        contra = entry_contra.get().strip()

        if not nombre or not contra:
            messagebox.showwarning("Campos vacios", "Por favor llena usuario y contrasena.")
            return

        if numero == 2 and self.jugador1 and nombre == self.jugador1["nombre"]:
            messagebox.showerror("Error", "El Jugador 2 no puede ser el mismo que el Jugador 1.")
            return

        jugador = iniciar_sesion(nombre, contra)
        if jugador:
            if numero == 1:
                self.jugador1 = jugador
            else:
                self.jugador2 = jugador
            label_estado.config(text=f"{nombre} conectado", fg=COLOR_EXITO)
            self.btn_avanzar.config(state="normal")
        else:
            messagebox.showerror("Error", "Usuario o contrasena incorrectos.")

    def _registrar(self, entry_usuario, entry_contra):
        nombre = entry_usuario.get().strip()
        contra = entry_contra.get().strip()

        if not nombre or not contra:
            messagebox.showwarning("Campos vacios", "Por favor llena usuario y contrasena.")
            return

        exito = registrar_jugador(nombre, contra)
        if exito:
            messagebox.showinfo("Registro exitoso", f"Jugador '{nombre}' registrado. Ya puedes iniciar sesion.")
        else:
            messagebox.showerror("Error", f"El usuario '{nombre}' ya existe.")

    def _iniciar_partida(self):
        self.frame.destroy()
        self.callback_login(self.jugador1, self.jugador2)