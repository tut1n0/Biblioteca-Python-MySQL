import customtkinter as ctk
from tkinter import ttk, messagebox

from controladores.libro_controller import (
    guardar_libro,
    obtener_libros,
    actualizar_libro,
    eliminar_libro
)

from controladores.autor_controller import obtener_autores_combo
from controladores.editorial_controller import obtener_editoriales
from controladores.categoria_controller import obtener_categorias


class LibrosFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.id_libro = None

        self.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ===========================
        # Diccionarios para Combobox
        # ===========================

        self.autores = {}
        self.editoriales = {}
        self.categorias = {}

        # ===========================
        # Título
        # ===========================

        ctk.CTkLabel(
            self,
            text="Gestión de Libros",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

        # ===========================
        # Formulario
        # ===========================

        formulario = ctk.CTkFrame(self)

        formulario.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # ---------------------------
        # Título
        # ---------------------------

        ctk.CTkLabel(
            formulario,
            text="Título"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        self.titulo = ctk.CTkEntry(
            formulario,
            width=260
        )

        self.titulo.grid(
            row=1,
            column=0,
            padx=10,
            pady=5
        )

        # ---------------------------
        # ISBN
        # ---------------------------

        ctk.CTkLabel(
            formulario,
            text="ISBN"
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        self.isbn = ctk.CTkEntry(
            formulario,
            width=170
        )

        self.isbn.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        # ---------------------------
        # Año
        # ---------------------------

        ctk.CTkLabel(
            formulario,
            text="Año"
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        self.anio = ctk.CTkEntry(
            formulario,
            width=80
        )

        self.anio.grid(
            row=1,
            column=2,
            padx=10,
            pady=5
        )

        # ---------------------------
        # Stock
        # ---------------------------

        ctk.CTkLabel(
            formulario,
            text="Stock"
        ).grid(
            row=0,
            column=3,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        self.stock = ctk.CTkEntry(
            formulario,
            width=80
        )

        self.stock.grid(
            row=1,
            column=3,
            padx=10,
            pady=5
        )

        # ===========================
        # Segunda fila
        # ===========================

        # Autor

        ctk.CTkLabel(
            formulario,
            text="Autor"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        self.combo_autor = ctk.CTkComboBox(
            formulario,
            width=260,
            state="readonly"
        )

        self.combo_autor.grid(
            row=3,
            column=0,
            padx=10,
            pady=5
        )

        # Editorial

        ctk.CTkLabel(
            formulario,
            text="Editorial"
        ).grid(
            row=2,
            column=1,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        self.combo_editorial = ctk.CTkComboBox(
            formulario,
            width=170,
            state="readonly"
        )

        self.combo_editorial.grid(
            row=3,
            column=1,
            padx=10,
            pady=5
        )

        # Categoría

        ctk.CTkLabel(
            formulario,
            text="Categoría"
        ).grid(
            row=2,
            column=2,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        self.combo_categoria = ctk.CTkComboBox(
            formulario,
            width=170,
            state="readonly"
        )

        self.combo_categoria.grid(
            row=3,
            column=2,
            padx=10,
            pady=5
        )

        
        # ===========================
        # BOTONES
        # ===========================

        botones = ctk.CTkFrame(self)

        botones.pack(
            pady=15
        )

        self.btn_nuevo = ctk.CTkButton(
            botones,
            text="Nuevo",
            command=self.nuevo
        )

        self.btn_nuevo.grid(
            row=0,
            column=0,
            padx=5
        )

        self.btn_guardar = ctk.CTkButton(
            botones,
            text="Guardar",
            command=self.guardar
        )

        self.btn_guardar.grid(
            row=0,
            column=1,
            padx=5
        )

        self.btn_modificar = ctk.CTkButton(
            botones,
            text="Modificar",
            command=self.modificar,
            state="disabled"
        )

        self.btn_modificar.grid(
            row=0,
            column=2,
            padx=5
        )

        self.btn_eliminar = ctk.CTkButton(
            botones,
            text="Eliminar",
            command=self.eliminar,
            fg_color="firebrick",
            hover_color="#8B0000",
            state="disabled"
        )

        self.btn_eliminar.grid(
            row=0,
            column=3,
            padx=5
        )

        # ===========================
        # TABLA
        # ===========================

        self.tabla = ttk.Treeview(
            self,
            columns=(
                "id",
                "titulo",
                "isbn",
                "anio",
                "stock",
                "autor",
                "editorial",
                "categoria"
            ),
            show="headings",
            height=12
        )

        columnas = {
            "id": ("ID", 60),
            "titulo": ("Título", 220),
            "isbn": ("ISBN", 150),
            "anio": ("Año", 70),
            "stock": ("Stock", 70),
            "autor": ("Autor", 180),
            "editorial": ("Editorial", 150),
            "categoria": ("Categoría", 150)
        }

        for columna, (texto, ancho) in columnas.items():

            self.tabla.heading(
                columna,
                text=texto
            )

            self.tabla.column(
                columna,
                width=ancho,
                anchor="center"
            )

        self.tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_libro
        )

        # ===========================
        # CARGA INICIAL
        # ===========================

        self.cargar_combos()
        self.cargar_libros()

    def nuevo(self):
        """Limpia el formulario para un nuevo registro."""

        self.id_libro = None

        self.titulo.delete(0, "end")
        self.isbn.delete(0, "end")
        self.anio.delete(0, "end")
        self.stock.delete(0, "end")

        if self.combo_autor.cget("values"):
            self.combo_autor.set(self.combo_autor.cget("values")[0])

        if self.combo_editorial.cget("values"):
            self.combo_editorial.set(self.combo_editorial.cget("values")[0])

        if self.combo_categoria.cget("values"):
            self.combo_categoria.set(self.combo_categoria.cget("values")[0])

        self.btn_guardar.configure(state="normal")
        self.btn_modificar.configure(state="disabled")
        self.btn_eliminar.configure(state="disabled")

        self.titulo.focus()


    def cargar_combos(self):
        """Carga autores, editoriales y categorías."""

        # ---------- AUTORES ----------

        autores = obtener_autores_combo()

        self.autores.clear()

        nombres_autores = []

        for id_autor, nombre in autores:

            self.autores[nombre] = id_autor
            nombres_autores.append(nombre)

        self.combo_autor.configure(
            values=nombres_autores
        )

        if nombres_autores:
            self.combo_autor.set(nombres_autores[0])

        # ---------- EDITORIALES ----------

        editoriales = obtener_editoriales()

        self.editoriales.clear()

        nombres_editoriales = []

        for id_editorial, nombre in editoriales:

            self.editoriales[nombre] = id_editorial
            nombres_editoriales.append(nombre)

        self.combo_editorial.configure(
            values=nombres_editoriales
        )

        if nombres_editoriales:
            self.combo_editorial.set(
                nombres_editoriales[0]
            )

        # ---------- CATEGORÍAS ----------

        categorias = obtener_categorias()

        self.categorias.clear()

        nombres_categorias = []

        for id_categoria, nombre in categorias:

            self.categorias[nombre] = id_categoria
            nombres_categorias.append(nombre)

        self.combo_categoria.configure(
            values=nombres_categorias
        )

        if nombres_categorias:
            self.combo_categoria.set(
                nombres_categorias[0]
            )


    def cargar_libros(self):
        """Carga los libros en la tabla."""

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        libros = obtener_libros()

        for libro in libros:
            self.tabla.insert(
                "",
                "end",
                values=libro
            )
    
    def guardar(self):

        titulo = self.titulo.get().strip()
        isbn = self.isbn.get().strip()
        anio = self.anio.get().strip()
        stock = self.stock.get().strip()

        if titulo == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar un título."
            )
            return

        if stock == "":
            stock = 0

        autor = self.combo_autor.get()
        editorial = self.combo_editorial.get()
        categoria = self.combo_categoria.get()

        id_autor = self.autores.get(autor)
        id_editorial = self.editoriales.get(editorial)
        id_categoria = self.categorias.get(categoria)

        ok = guardar_libro(
            titulo,
            isbn,
            anio,
            stock,
            id_autor,
            id_editorial,
            id_categoria
        )

        if ok:

            messagebox.showinfo(
                "Correcto",
                "Libro guardado correctamente."
            )

            self.nuevo()
            self.cargar_libros()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible guardar el libro.")


    def seleccionar_libro(self, event):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        self.id_libro = valores[0]

        self.titulo.delete(0, "end")
        self.titulo.insert(0, valores[1])

        self.isbn.delete(0, "end")
        self.isbn.insert(0, valores[2])

        self.anio.delete(0, "end")
        self.anio.insert(0, valores[3])

        self.stock.delete(0, "end")
        self.stock.insert(0, valores[4])

        if len(valores) >= 8:

            self.combo_autor.set(valores[5])
            self.combo_editorial.set(valores[6])
            self.combo_categoria.set(valores[7])

        self.btn_guardar.configure(state="disabled")
        self.btn_modificar.configure(state="normal")
        self.btn_eliminar.configure(state="normal")


    def modificar(self):

        if self.id_libro is None:
            return

        titulo = self.titulo.get().strip()
        isbn = self.isbn.get().strip()
        anio = self.anio.get().strip()
        stock = self.stock.get().strip()

        if titulo == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar un título."
            )
            return

        if stock == "":
            stock = 0

        autor = self.combo_autor.get()
        editorial = self.combo_editorial.get()
        categoria = self.combo_categoria.get()

        id_autor = self.autores.get(autor)
        id_editorial = self.editoriales.get(editorial)
        id_categoria = self.categorias.get(categoria)

        ok = actualizar_libro(
            self.id_libro,
            titulo,
            isbn,
            anio,
            stock,
            id_autor,
            id_editorial,
            id_categoria
        )

        if ok:

            messagebox.showinfo(
                "Correcto",
                "Libro actualizado correctamente."
            )

            self.nuevo()
            self.cargar_libros()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible actualizar el libro."
            )


    def eliminar(self):

        if self.id_libro is None:
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar este libro?"
        )

        if not respuesta:
            return

        ok = eliminar_libro(self.id_libro)

        if ok:

            messagebox.showinfo(
                "Correcto",
                "Libro eliminado correctamente."
            )

            self.nuevo()
            self.cargar_libros()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible eliminar el libro."
            )