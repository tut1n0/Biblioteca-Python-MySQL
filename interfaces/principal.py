import customtkinter as ctk

from interfaces.libros import LibrosFrame, LibrosCatalogoFrame
from interfaces.autores import AutoresFrame
from interfaces.editoriales import EditorialesFrame
from interfaces.categorias import CategoriasFrame
from interfaces.socios import SociosFrame
from interfaces.prestamos import PrestamosFrame
from interfaces.empleados import EmpleadosFrame


class Principal:

    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.ventana = ctk.CTk()

        self.ventana.title("Sistema Biblioteca")
        self.ventana.geometry("1100x650")
        self.ventana.minsize(1000, 600)

        self.crear_menu()
        self.crear_area_principal()

        self.ventana.mainloop()

    def crear_menu(self):
        self.menu = ctk.CTkFrame(
            self.ventana,
            width=220,
            corner_radius=0,
            fg_color="#1f4e79"
        )

        self.menu.pack(
            side="left",
            fill="y"
        )

        self.menu.pack_propagate(False)

        ctk.CTkButton(
            self.menu,
            text="BIBLIOTECA",
            height=45,
            fg_color="transparent",
            hover_color="#1e40af",
            text_color="white",
            font=("Arial", 22, "bold"),
            anchor="w",
            command=self.mostrar_bienvenida
        ).pack(pady=(28, 4), fill="x", padx=16)

        ctk.CTkLabel(
            self.menu,
            text="Panel administrativo",
            font=("Arial", 12),
            text_color="#dbeafe"
        ).pack(pady=(0, 25))

        self.crear_boton_menu("Libros", self.vista_libros)
        self.crear_boton_menu("Autores", self.vista_autores)
        self.crear_boton_menu("Editoriales", self.vista_editoriales)
        self.crear_boton_menu("Categorías", self.vista_categorias)
        self.crear_boton_menu("Socios", self.vista_socios)
        self.crear_boton_menu("Préstamos", self.vista_prestamos)
        self.crear_boton_menu("Empleados", self.vista_empleados)

        ctk.CTkButton(
            self.menu,
            text="Salir",
            height=38,
            fg_color="#b91c1c",
            hover_color="#7f1d1d",
            command=self.ventana.destroy
        ).pack(
            side="bottom",
            fill="x",
            padx=18,
            pady=22
        )

    def crear_boton_menu(self, texto, comando):
        ctk.CTkButton(
            self.menu,
            text=texto,
            height=38,
            anchor="w",
            fg_color="transparent",
            hover_color="#2563eb",
            text_color="white",
            font=("Arial", 14),
            command=comando
        ).pack(fill="x", padx=16, pady=4)

    def crear_area_principal(self):
        self.area = ctk.CTkFrame(
            self.ventana,
            fg_color="#f3f6fb",
            corner_radius=0
        )

        self.area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.mostrar_bienvenida()

    def limpiar_area(self):
        for widget in self.area.winfo_children():
            widget.destroy()

    def mostrar_frame(self, frame):
        self.limpiar_area()
        frame(self.area)

    def mostrar_bienvenida(self):
        self.limpiar_area()

        contenedor = ctk.CTkFrame(
            self.area,
            fg_color="transparent"
        )
        contenedor.pack(fill="both", expand=True, padx=40, pady=40)

        ctk.CTkLabel(
            contenedor,
            text="Bienvenido al Sistema Biblioteca",
            font=("Arial", 28, "bold"),
            text_color="#1f2937"
        ).pack(anchor="w", pady=(10, 8))

        ctk.CTkLabel(
            contenedor,
            text="Administrá libros, socios, préstamos y usuarios desde un solo panel.",
            font=("Arial", 15),
            text_color="#4b5563"
        ).pack(anchor="w", pady=(0, 30))

        tarjetas = ctk.CTkFrame(
            contenedor,
            fg_color="transparent"
        )
        tarjetas.pack(fill="x", pady=10)

        self.crear_tarjeta_resumen(
            tarjetas,
            "Catálogo",
            "Libros, autores, editoriales y categorías.",
            0,
            self.vista_catalogo
        )

        self.crear_tarjeta_resumen(
            tarjetas,
            "Circulación",
            "Socios, préstamos y control de stock.",
            1
        )

        self.crear_tarjeta_resumen(
            tarjetas,
            "Administración",
            "Empleados y acceso al sistema.",
            2
        )

    def crear_tarjeta_resumen(self, master, titulo, texto, columna, comando=None):
        tarjeta = ctk.CTkFrame(
            master,
            corner_radius=10,
            fg_color="white"
        )

        tarjeta.grid(
            row=0,
            column=columna,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        master.grid_columnconfigure(columna, weight=1)

        ctk.CTkLabel(
            tarjeta,
            text=titulo,
            font=("Arial", 18, "bold"),
            text_color="#1f4e79"
        ).pack(anchor="w", padx=20, pady=(20, 8))

        ctk.CTkLabel(
            tarjeta,
            text=texto,
            font=("Arial", 13),
            text_color="#555555",
            wraplength=230,
            justify="left"
        ).pack(anchor="w", padx=20, pady=(0, 22))

        if comando:
            ctk.CTkButton(
                tarjeta,
                text="Ver libros",
                fg_color="#1e40af",
                hover_color="#2563eb",
                text_color="white",
                command=comando
            ).pack(padx=20, pady=(0, 20), fill="x")

    def vista_libros(self):
        self.mostrar_frame(LibrosFrame)

    def vista_catalogo(self):
        self.mostrar_frame(LibrosCatalogoFrame)

    def vista_autores(self):
        self.mostrar_frame(AutoresFrame)

    def vista_editoriales(self):
        self.mostrar_frame(EditorialesFrame)

    def vista_categorias(self):
        self.mostrar_frame(CategoriasFrame)

    def vista_socios(self):
        self.mostrar_frame(SociosFrame)

    def vista_prestamos(self):
        self.mostrar_frame(PrestamosFrame)

    def vista_empleados(self):
        self.mostrar_frame(EmpleadosFrame)