import customtkinter as ctk

from interfaces.libros import LibrosFrame
from interfaces.autores import AutoresFrame
from interfaces.editoriales import EditorialesFrame
from interfaces.categorias import CategoriasFrame

class Principal:

    def __init__(self):

        self.ventana = ctk.CTk()

        self.ventana.title("Sistema Biblioteca")
        self.ventana.geometry("900x500")

        self.crear_menu()
        self.crear_area_principal()

        self.ventana.mainloop()

    # ==========================================
    # MENÚ
    # ==========================================

    def crear_menu(self):

        self.menu = ctk.CTkFrame(
            self.ventana,
            width=200
        )

        self.menu.pack(
            side="left",
            fill="y"
        )

        ctk.CTkLabel(
            self.menu,
            text="📚 BIBLIOTECA",
            font=("Arial", 20, "bold")
        ).pack(pady=25)

        ctk.CTkButton(
            self.menu,
            text="Libros",
            command=lambda: self.mostrar_frame(LibrosFrame)
        ).pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(
            self.menu,
            text="Autores",
            command=lambda: self.mostrar_frame(AutoresFrame)
        ).pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(
            self.menu,
            text="Editoriales",
            command=self.vista_editoriales
        ).pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(
            self.menu,
            text="Categorías",
            command=self.vista_categorias
        ).pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(
            self.menu,
            text="Socios",
            command=self.vista_socios
        ).pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(
            self.menu,
            text="Préstamos",
            command=self.vista_prestamos
        ).pack(fill="x", padx=15, pady=5)

        ctk.CTkButton(
            self.menu,
            text="Salir",
            fg_color="red",
            command=self.ventana.destroy
        ).pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=20
        )

    # ==========================================
    # ÁREA PRINCIPAL
    # ==========================================

    def crear_area_principal(self):

        self.area = ctk.CTkFrame(self.ventana)

        self.area.pack(
            side="right",
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            self.area,
            text="Bienvenido al Sistema Biblioteca",
            font=("Arial", 24, "bold")
        ).pack(pady=60)

    # ==========================================
    # UTILIDADES
    # ==========================================

    def limpiar_area(self):

        for widget in self.area.winfo_children():
            widget.destroy()

    def mostrar_frame(self, frame):

        self.limpiar_area()

        frame(self.area)

    # ==========================================
    # VISTAS
    # ==========================================

    def vista_editoriales(self):

        self.mostrar_frame(EditorialesFrame)

        ctk.CTkLabel(
            self.area,
            text="Gestión de Editoriales",
            font=("Arial", 20)
        ).pack(pady=20)

    def vista_categorias(self):

        self.mostrar_frame(CategoriasFrame)

        ctk.CTkLabel(
            self.area,
            text="Gestión de Categorías",
            font=("Arial", 20)
        ).pack(pady=20)

    def vista_socios(self):

        self.limpiar_area()

        ctk.CTkLabel(
            self.area,
            text="Gestión de Socios",
            font=("Arial", 20)
        ).pack(pady=20)

    def vista_prestamos(self):

        self.limpiar_area()

        ctk.CTkLabel(
            self.area,
            text="Gestión de Préstamos",
            font=("Arial", 20)
        ).pack(pady=20)