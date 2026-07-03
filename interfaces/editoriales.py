import customtkinter as ctk
from tkinter import ttk, messagebox

from controladores.editorial_controller import (
    guardar_editorial,
    obtener_editoriales,
    actualizar_editorial,
    eliminar_editorial
)


class EditorialesFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.id_editorial = None
        self.editoriales_cache = []

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
            text="Gestión de Editoriales",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

        # ===============================
        # BÚSQUEDA
        # ===============================

        busqueda_frame = ctk.CTkFrame(self)
        busqueda_frame.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(
            busqueda_frame,
            text="Buscar editoriales"
        ).grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")

        self.busqueda_editorial = ctk.CTkEntry(
            busqueda_frame,
            placeholder_text="Nombre o ID"
        )
        self.busqueda_editorial.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        busqueda_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            busqueda_frame,
            text="Limpiar",
            width=90,
            command=self.limpiar_busqueda
        ).grid(row=0, column=2, padx=5, pady=5)

        self.busqueda_editorial.bind("<KeyRelease>", self.filtrar_editoriales)

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
            self.seleccionar_editorial
        )

        self.cargar_editoriales()

    def nuevo(self):
            """Limpia el formulario para ingresar una nueva editorial."""

            self.id_editorial = None

            self.nombre.delete(0, "end")

            self.btn_guardar.configure(state="normal")
            self.btn_modificar.configure(state="disabled")
            self.btn_eliminar.configure(state="disabled")

            self.nombre.focus()

    def cargar_editoriales(self):
        """Carga todas las editoriales en la tabla."""

        self.editoriales_cache = obtener_editoriales()
        self._actualizar_tabla_editoriales(self.editoriales_cache)

    def _actualizar_tabla_editoriales(self, editoriales):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for editorial in editoriales:
            self.tabla.insert("", "end", values=editorial)

    def filtrar_editoriales(self, event=None):
        texto = self.busqueda_editorial.get().strip().lower()

        if texto == "":
            self._actualizar_tabla_editoriales(self.editoriales_cache)
            return

        filtrados = [
            editorial for editorial in self.editoriales_cache
            if texto in " ".join(map(str, editorial)).lower()
        ]

        self._actualizar_tabla_editoriales(filtrados)

    def limpiar_busqueda(self):
        self.busqueda_editorial.delete(0, "end")
        self.filtrar_editoriales()

    def guardar(self):

        nombre = self.nombre.get().strip()

        if nombre == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar el nombre de la editorial."
            )
            return

        ok = guardar_editorial(nombre)

        if ok:

            messagebox.showinfo(
                "Correcto",
                "Editorial guardada correctamente."
            )

            self.nuevo()
            self.cargar_editoriales()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible guardar la editorial."
            )

    def seleccionar_editorial(self, event):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        self.id_editorial = valores[0]

        self.nombre.delete(0, "end")
        self.nombre.insert(0, valores[1])

        self.btn_guardar.configure(state="disabled")
        self.btn_modificar.configure(state="normal")
        self.btn_eliminar.configure(state="normal")

    def modificar(self):

        if self.id_editorial is None:
            return

        nombre = self.nombre.get().strip()

        if nombre == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar el nombre de la editorial."
            )
            return

        ok = actualizar_editorial(
            self.id_editorial,
            nombre
        )

        if ok:

            messagebox.showinfo(
                "Correcto",
                "Editorial actualizada correctamente."
            )

            self.nuevo()
            self.cargar_editoriales()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible actualizar la editorial."
            )

    def eliminar(self):

        if self.id_editorial is None:
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar esta editorial?"
        )

        if not respuesta:
            return

        ok = eliminar_editorial(
            self.id_editorial
        )

        if ok:

            messagebox.showinfo(
                "Correcto",
                "Editorial eliminada correctamente."
            )

            self.nuevo()
            self.cargar_editoriales()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible eliminar la editorial."
            )