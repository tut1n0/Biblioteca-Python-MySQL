import customtkinter as ctk
from conexion import conectar


class LoginApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.ventana = ctk.CTk()
        self.ventana.title("Biblioteca - Inicio de sesión")
        self.ventana.geometry("420x420")
        self.ventana.resizable(False, False)

        self.crear_widgets()

        self.ventana.mainloop()

    def crear_widgets(self):
        contenedor = ctk.CTkFrame(
            self.ventana,
            fg_color="transparent"
        )
        contenedor.pack(fill="both", expand=True, padx=35, pady=35)

        ctk.CTkLabel(
            contenedor,
            text="BIBLIOTECA",
            font=("Arial", 28, "bold"),
            text_color="#1f4e79"
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            contenedor,
            text="Sistema de gestión",
            font=("Arial", 14),
            text_color="#555555"
        ).pack(pady=(0, 25))

        tarjeta = ctk.CTkFrame(
            contenedor,
            corner_radius=12
        )
        tarjeta.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(
            tarjeta,
            text="Iniciar sesión",
            font=("Arial", 20, "bold")
        ).pack(pady=(25, 15))

        self.usuario = ctk.CTkEntry(
            tarjeta,
            width=260,
            height=38,
            placeholder_text="Usuario"
        )
        self.usuario.pack(pady=8)

        self.password = ctk.CTkEntry(
            tarjeta,
            width=260,
            height=38,
            placeholder_text="Contraseña",
            show="*"
        )
        self.password.pack(pady=8)

        ctk.CTkButton(
            tarjeta,
            text="Ingresar",
            width=260,
            height=38,
            command=self.validar
        ).pack(pady=(18, 10))

        self.mensaje = ctk.CTkLabel(
            tarjeta,
            text="",
            font=("Arial", 12)
        )
        self.mensaje.pack(pady=(5, 15))

        self.usuario.focus()

    def validar(self):
        user = self.usuario.get().strip()
        password = self.password.get().strip()

        if user == "" or password == "":
            self.mensaje.configure(
                text="Ingresá usuario y contraseña.",
                text_color="firebrick"
            )
            return

        conn = conectar()

        if conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM empleados WHERE usuario=%s AND password=%s",
                (user, password)
            )

            resultado = cursor.fetchone()

            cursor.close()
            conn.close()

            if resultado:
                self.mensaje.configure(
                    text="Acceso correcto.",
                    text_color="green"
                )

                self.ventana.destroy()

                import interfaces.principal
                interfaces.principal.Principal()

            else:
                self.mensaje.configure(
                    text="Usuario o contraseña incorrectos.",
                    text_color="firebrick"
                )
        else:
            self.mensaje.configure(
                text="No se pudo conectar a la base de datos.",
                text_color="firebrick"
            )