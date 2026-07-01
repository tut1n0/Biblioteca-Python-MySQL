import customtkinter as ctk
from tkinter import ttk, messagebox

from controladores.categoria_controller import (
    guardar_categoria,
    obtener_categorias,
    actualizar_categoria,
    eliminar_categoria
)

class CategoriasFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.id_categoria = None

        self.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ===============================
        # TÍTULO
        # ===============================

        ctk.CTkLabel(
            self,
            text="Gestión de Categorías",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

        # ===============================
        # FORMULARIO
        # ===============================

        formulario = ctk.CTkFrame(self)

        formulario.pack(
            fill="x",
            padx=20,
            pady=10
        )

        # Nombre

        ctk.CTkLabel(
            formulario,
            text="Nombre"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        self.nombre = ctk.CTkEntry(
            formulario,
            width=350
        )

        self.nombre.grid(
            row=1,
            column=0,
            padx=10,
            pady=5
        )

        # ===============================
        # BOTONES
        # ===============================

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

        # ===============================
        # TABLA
        # ===============================

        self.tabla = ttk.Treeview(
            self,
            columns=(
                "id",
                "nombre"
            ),
            show="headings",
            height=12
        )

        self.tabla.heading(
            "id",
            text="ID"
        )

        self.tabla.heading(
            "nombre",
            text="Nombre"
        )

        self.tabla.column(
            "id",
            width=80,
            anchor="center"
        )

        self.tabla.column(
            "nombre",
            width=450
        )

        self.tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_categoria
        )

        self.cargar_categorias()

    def nuevo(self):
            """Limpia el formulario para ingresar una nueva categoría."""

            self.id_categoria = None

            self.nombre.delete(0, "end")

            self.btn_guardar.configure(state="normal")
            self.btn_modificar.configure(state="disabled")
            self.btn_eliminar.configure(state="disabled")

            self.nombre.focus()

    def cargar_categorias(self):
        """Carga todas las categorías en la tabla."""

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        categorias = obtener_categorias()

        for categoria in categorias:
            self.tabla.insert("", "end", values=categoria)

    def guardar(self):

        nombre = self.nombre.get().strip()

        if nombre == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar el nombre de la categoria."
            )
            return

        ok = guardar_categoria(nombre)

        if ok:

            messagebox.showinfo(
                "Correcto",
                "Categoría guardada correctamente."
            )

            self.nuevo()
            self.cargar_categorias()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible guardar la categoria."
            )

    def seleccionar_categoria(self, event):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        self.id_categoria = valores[0]

        self.nombre.delete(0, "end")
        self.nombre.insert(0, valores[1])

        self.btn_guardar.configure(state="disabled")
        self.btn_modificar.configure(state="normal")
        self.btn_eliminar.configure(state="normal")

    def modificar(self):

        if self.id_categoria is None:
            return

        nombre = self.nombre.get().strip()

        if nombre == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar el nombre de la categoria."
            )
            return

        ok = actualizar_categoria(
            self.id_categoria,
            nombre
        )

        if ok:

            messagebox.showinfo(
                "Correcto",
                "Categoría actualizada correctamente."
            )

            self.nuevo()
            self.cargar_categorias()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible actualizar la categoria."
            )

    def eliminar(self):

        if self.id_categoria is None:
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar esta categoria?"
        )

        if not respuesta:
            return

        ok = eliminar_categoria(
            self.id_categoria
        )

        if ok:

            messagebox.showinfo(
                "Correcto",
                "Categoría eliminada correctamente."
            )

            self.nuevo()
            self.cargar_categorias()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible eliminar la categoria."
            )