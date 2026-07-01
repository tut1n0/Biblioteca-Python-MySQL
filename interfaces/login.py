import customtkinter as ctk
from conexion import conectar


class LoginApp:
    def __init__(self):
        self.ventana = ctk.CTk()
        self.ventana.title("Login Biblioteca")
        self.ventana.geometry("400x300")
        self.ventana.resizable(False, False)

        self.crear_widgets()

        self.ventana.mainloop()

    def crear_widgets(self):

        ctk.CTkLabel(self.ventana, text="INICIO DE SESIÓN", font=("Arial", 20)).pack(pady=20)

        self.usuario = ctk.CTkEntry(self.ventana, placeholder_text="Usuario")
        self.usuario.pack(pady=10)

        self.password = ctk.CTkEntry(self.ventana, placeholder_text="Contraseña", show="*")
        self.password.pack(pady=10)

        ctk.CTkButton(self.ventana, text="Ingresar", command=self.validar).pack(pady=20)

        self.mensaje = ctk.CTkLabel(self.ventana, text="")
        self.mensaje.pack()

    def validar(self):
        user = self.usuario.get()
        password = self.password.get()

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
                self.mensaje.configure(text="Login correcto ✅", text_color="green")
                print("Acceso permitido")
                self.ventana.destroy()
                import interfaces.principal
                interfaces.principal.Principal()

            else:
                self.mensaje.configure(text="Usuario o contraseña incorrectos ❌", text_color="red")