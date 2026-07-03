import customtkinter as ctk
from tkinter import ttk, messagebox

from controladores.autor_controller import (
    guardar_autor,
    obtener_autores,
    actualizar_autor,
    eliminar_autor
)


class AutoresFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.id_autor = None
        self.autores_cache = []

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
            text="Gestión de Autores",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

        # ===============================
        # BÚSQUEDA
        # ===============================

        busqueda_frame = ctk.CTkFrame(self)
        busqueda_frame.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(
            busqueda_frame,
            text="Buscar autores"
        ).grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")

        self.busqueda_autor = ctk.CTkEntry(
            busqueda_frame,
            placeholder_text="Nombre, nacionalidad o ID"
        )
        self.busqueda_autor.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        busqueda_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            busqueda_frame,
            text="Limpiar",
            width=90,
            command=self.limpiar_busqueda
        ).grid(row=0, column=2, padx=5, pady=5)

        self.busqueda_autor.bind("<KeyRelease>", self.filtrar_autores)

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
            width=280
        )

        self.nombre.grid(
            row=1,
            column=0,
            padx=10,
            pady=5
        )

        # Nacionalidad

        ctk.CTkLabel(
            formulario,
            text="Nacionalidad"
        ).grid(
            row=0,
            column=1,
            padx=10,
            pady=(15, 5),
            sticky="w"
        )

        self.nacionalidad = ctk.CTkEntry(
            formulario,
            width=180
        )

        self.nacionalidad.grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        # ===============================
        # BOTONES
        # ===============================

        botones = ctk.CTkFrame(self)

        botones.pack(pady=15)

        self.btn_nuevo = ctk.CTkButton(
            botones,
            text="Nuevo",
            command=self.nuevo
        )

        self.btn_nuevo.grid(row=0, column=0, padx=5)

        self.btn_guardar = ctk.CTkButton(
            botones,
            text="Guardar",
            command=self.guardar
        )

        self.btn_guardar.grid(row=0, column=1, padx=5)

        self.btn_modificar = ctk.CTkButton(
            botones,
            text="Modificar",
            command=self.modificar,
            state="disabled"
        )

        self.btn_modificar.grid(row=0, column=2, padx=5)

        self.btn_eliminar = ctk.CTkButton(
            botones,
            text="Eliminar",
            command=self.eliminar,
            fg_color="firebrick",
            hover_color="#8B0000",
            state="disabled"
        )

        self.btn_eliminar.grid(row=0, column=3, padx=5)

        # ===============================
        # TABLA
        # ===============================

        self.tabla = ttk.Treeview(
            self,
            columns=(
                "id",
                "nombre",
                "nacionalidad"
            ),
            show="headings",
            height=12
        )

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("nacionalidad", text="Nacionalidad")

        self.tabla.column(
            "id",
            width=70,
            anchor="center"
        )

        self.tabla.column(
            "nombre",
            width=320
        )

        self.tabla.column(
            "nacionalidad",
            width=180
        )

        self.tabla.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.seleccionar_autor
        )

        self.cargar_autores()


    def nuevo(self):
        """Limpia el formulario para ingresar un nuevo autor."""

        self.id_autor = None

        self.nombre.delete(0, "end")
        self.nacionalidad.delete(0, "end")

        self.btn_guardar.configure(state="normal")
        self.btn_modificar.configure(state="disabled")
        self.btn_eliminar.configure(state="disabled")

        self.nombre.focus()

    def cargar_autores(self):
        """Carga todos los autores en la tabla."""

        self.autores_cache = obtener_autores()
        self._actualizar_tabla_autores(self.autores_cache)

    def _actualizar_tabla_autores(self, autores):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for autor in autores:
            self.tabla.insert("", "end", values=autor)

    def filtrar_autores(self, event=None):
        texto = self.busqueda_autor.get().strip().lower()

        if texto == "":
            self._actualizar_tabla_autores(self.autores_cache)
            return

        filtrados = [
            autor for autor in self.autores_cache
            if texto in " ".join(map(str, autor)).lower()
        ]

        self._actualizar_tabla_autores(filtrados)

    def limpiar_busqueda(self):
        self.busqueda_autor.delete(0, "end")
        self.filtrar_autores()

    def guardar(self):

        nombre = self.nombre.get().strip()
        nacionalidad = self.nacionalidad.get().strip()

        if nombre == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar el nombre del autor."
            )
            return

        ok = guardar_autor(
            nombre,
            nacionalidad
        )

        if ok:

            messagebox.showinfo(
                "Correcto",
                "Autor guardado correctamente."
            )

            self.nuevo()
            self.cargar_autores()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible guardar el autor."
            )

    def seleccionar_autor(self, event):

        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(
            seleccion[0],
            "values"
        )

        self.id_autor = valores[0]

        self.nombre.delete(0, "end")
        self.nombre.insert(0, valores[1])

        self.nacionalidad.delete(0, "end")
        self.nacionalidad.insert(0, valores[2])

        self.btn_guardar.configure(state="disabled")
        self.btn_modificar.configure(state="normal")
        self.btn_eliminar.configure(state="normal")

    def modificar(self):

        if self.id_autor is None:
            return

        nombre = self.nombre.get().strip()
        nacionalidad = self.nacionalidad.get().strip()

        if nombre == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar el nombre del autor."
            )
            return

        ok = actualizar_autor(
            self.id_autor,
            nombre,
            nacionalidad
        )

        if ok:

            messagebox.showinfo(
                "Correcto",
                "Autor actualizado correctamente."
            )

            self.nuevo()
            self.cargar_autores()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible actualizar el autor."
            )

    def eliminar(self):

        if self.id_autor is None:
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar este autor?"
        )

        if not respuesta:
            return

        ok = eliminar_autor(
            self.id_autor
        )

        if ok:

            messagebox.showinfo(
                "Correcto",
                "Autor eliminado correctamente."
            )

            self.nuevo()
            self.cargar_autores()

        else:

            messagebox.showerror(
                "Error",
                "No fue posible eliminar el autor."
            )