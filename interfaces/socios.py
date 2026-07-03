import customtkinter as ctk
from tkinter import ttk, messagebox

from controladores.socio_controller import (
    guardar_socio,
    obtener_socios,
    actualizar_socio,
    eliminar_socio
)


class SociosFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.id_socio = None
        self.socios_cache = []

        self.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            self,
            text="Gestión de Socios",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

        # ===============================
        # BÚSQUEDA
        # ===============================

        busqueda_frame = ctk.CTkFrame(self)
        busqueda_frame.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(
            busqueda_frame,
            text="Buscar socios"
        ).grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")

        self.busqueda_socio = ctk.CTkEntry(
            busqueda_frame,
            placeholder_text="Nombre, apellido, DNI o email"
        )
        self.busqueda_socio.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        busqueda_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkButton(
            busqueda_frame,
            text="Limpiar",
            width=90,
            command=self.limpiar_busqueda
        ).grid(row=0, column=2, padx=5, pady=5)

        self.busqueda_socio.bind("<KeyRelease>", self.filtrar_socios)

        formulario = ctk.CTkFrame(self)
        formulario.pack(fill="x", padx=20, pady=10)

        campos = [
            ("Nombre", "nombre", 0, 0, 180),
            ("Apellido", "apellido", 0, 1, 180),
            ("DNI", "dni", 0, 2, 130),
            ("Teléfono", "telefono", 1, 0, 160),
            ("Email", "email", 1, 1, 220),
            ("Dirección", "direccion", 1, 2, 240),
        ]

        for texto, atributo, fila, columna, ancho in campos:
            ctk.CTkLabel(formulario, text=texto).grid(
                row=fila * 2,
                column=columna,
                padx=10,
                pady=(15, 5),
                sticky="w"
            )

            entrada = ctk.CTkEntry(formulario, width=ancho)
            entrada.grid(
                row=fila * 2 + 1,
                column=columna,
                padx=10,
                pady=5
            )

            setattr(self, atributo, entrada)

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

        self.tabla = ttk.Treeview(
            self,
            columns=(
                "id",
                "nombre",
                "apellido",
                "dni",
                "telefono",
                "email",
                "direccion"
            ),
            show="headings",
            height=12
        )

        columnas = {
            "id": ("ID", 60),
            "nombre": ("Nombre", 150),
            "apellido": ("Apellido", 150),
            "dni": ("DNI", 110),
            "telefono": ("Teléfono", 130),
            "email": ("Email", 180),
            "direccion": ("Dirección", 220)
        }

        for columna, (texto, ancho) in columnas.items():
            self.tabla.heading(columna, text=texto)
            self.tabla.column(columna, width=ancho, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=20, pady=10)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_socio)

        self.cargar_socios()

    def cargar_socios(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        self.socios_cache = obtener_socios()

        for socio in self.socios_cache:
            self.tabla.insert("", "end", values=socio)

    def _actualizar_tabla_socios(self, socios):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for socio in socios:
            self.tabla.insert("", "end", values=socio)

    def filtrar_socios(self, event=None):
        texto = self.busqueda_socio.get().strip().lower()

        if texto == "":
            self._actualizar_tabla_socios(self.socios_cache)
            return

        filtrados = [
            socio for socio in self.socios_cache
            if texto in " ".join(map(str, socio)).lower()
        ]

        self._actualizar_tabla_socios(filtrados)

    def limpiar_busqueda(self):
        self.busqueda_socio.delete(0, "end")
        self.filtrar_socios()

    def nuevo(self):
        self.id_socio = None

        self.nombre.delete(0, "end")
        self.apellido.delete(0, "end")
        self.dni.delete(0, "end")
        self.telefono.delete(0, "end")
        self.email.delete(0, "end")
        self.direccion.delete(0, "end")

        self.btn_guardar.configure(state="normal")
        self.btn_modificar.configure(state="disabled")
        self.btn_eliminar.configure(state="disabled")

        self.nombre.focus()

    def guardar(self):
        nombre = self.nombre.get().strip()
        apellido = self.apellido.get().strip()
        dni = self.dni.get().strip()
        telefono = self.telefono.get().strip()
        email = self.email.get().strip()
        direccion = self.direccion.get().strip()

        if nombre == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar el nombre del socio."
            )
            return

        if apellido == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar el apellido del socio."
            )
            return

        ok = guardar_socio(
            nombre,
            apellido,
            dni,
            telefono,
            email,
            direccion
        )

        if ok:
            messagebox.showinfo(
                "Correcto",
                "Socio guardado correctamente."
            )

            self.nuevo()
            self.cargar_socios()

        else:
            messagebox.showerror(
                "Error",
                "No fue posible guardar el socio."
            )

    def seleccionar_socio(self, event):
        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(seleccion[0], "values")

        self.id_socio = valores[0]

        self.nombre.delete(0, "end")
        self.nombre.insert(0, valores[1])

        self.apellido.delete(0, "end")
        self.apellido.insert(0, valores[2])

        self.dni.delete(0, "end")
        self.dni.insert(0, valores[3])

        self.telefono.delete(0, "end")
        self.telefono.insert(0, valores[4])

        self.email.delete(0, "end")
        self.email.insert(0, valores[5])

        self.direccion.delete(0, "end")
        self.direccion.insert(0, valores[6])

        self.btn_guardar.configure(state="disabled")
        self.btn_modificar.configure(state="normal")
        self.btn_eliminar.configure(state="normal")

    def modificar(self):
        if self.id_socio is None:
            return

        nombre = self.nombre.get().strip()
        apellido = self.apellido.get().strip()
        dni = self.dni.get().strip()
        telefono = self.telefono.get().strip()
        email = self.email.get().strip()
        direccion = self.direccion.get().strip()

        if nombre == "" or apellido == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar nombre y apellido del socio."
            )
            return

        ok = actualizar_socio(
            self.id_socio,
            nombre,
            apellido,
            dni,
            telefono,
            email,
            direccion
        )

        if ok:
            messagebox.showinfo(
                "Correcto",
                "Socio actualizado correctamente."
            )

            self.nuevo()
            self.cargar_socios()

        else:
            messagebox.showerror(
                "Error",
                "No fue posible actualizar el socio."
            )

    def eliminar(self):
        if self.id_socio is None:
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar este socio?"
        )

        if not respuesta:
            return

        ok = eliminar_socio(self.id_socio)

        if ok:
            messagebox.showinfo(
                "Correcto",
                "Socio eliminado correctamente."
            )

            self.nuevo()
            self.cargar_socios()

        else:
            messagebox.showerror(
                "Error",
                "No fue posible eliminar el socio."
            )