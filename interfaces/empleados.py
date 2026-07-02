import customtkinter as ctk
from tkinter import ttk, messagebox

from controladores.empleado_controller import (
    guardar_empleado,
    obtener_empleados,
    actualizar_empleado,
    eliminar_empleado
)


class EmpleadosFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.id_empleado = None

        self.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            self,
            text="Gestión de Empleados",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

        formulario = ctk.CTkFrame(self)
        formulario.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(formulario, text="Nombre").grid(
            row=0, column=0, padx=10, pady=(15, 5), sticky="w"
        )

        self.nombre = ctk.CTkEntry(formulario, width=220)
        self.nombre.grid(row=1, column=0, padx=10, pady=5)

        ctk.CTkLabel(formulario, text="Usuario").grid(
            row=0, column=1, padx=10, pady=(15, 5), sticky="w"
        )

        self.usuario = ctk.CTkEntry(formulario, width=180)
        self.usuario.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(formulario, text="Contraseña").grid(
            row=0, column=2, padx=10, pady=(15, 5), sticky="w"
        )

        self.password = ctk.CTkEntry(formulario, width=180, show="*")
        self.password.grid(row=1, column=2, padx=10, pady=5)

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
                "usuario",
                "password"
            ),
            show="headings",
            height=12
        )

        columnas = {
            "id": ("ID", 70),
            "nombre": ("Nombre", 220),
            "usuario": ("Usuario", 180),
            "password": ("Contraseña", 180)
        }

        for columna, (texto, ancho) in columnas.items():
            self.tabla.heading(columna, text=texto)
            self.tabla.column(columna, width=ancho, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=20, pady=10)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_empleado)

        self.cargar_empleados()

    def nuevo(self):
        self.id_empleado = None

        self.nombre.delete(0, "end")
        self.usuario.delete(0, "end")
        self.password.delete(0, "end")

        self.btn_guardar.configure(state="normal")
        self.btn_modificar.configure(state="disabled")
        self.btn_eliminar.configure(state="disabled")

        self.nombre.focus()

    def cargar_empleados(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        empleados = obtener_empleados()

        for empleado in empleados:
            self.tabla.insert("", "end", values=empleado)

    def guardar(self):
        nombre = self.nombre.get().strip()
        usuario = self.usuario.get().strip()
        password = self.password.get().strip()

        if nombre == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar el nombre del empleado."
            )
            return

        if usuario == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar el usuario."
            )
            return

        if password == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar la contraseña."
            )
            return

        ok = guardar_empleado(nombre, usuario, password)

        if ok:
            messagebox.showinfo(
                "Correcto",
                "Empleado guardado correctamente."
            )

            self.nuevo()
            self.cargar_empleados()

        else:
            messagebox.showerror(
                "Error",
                "No fue posible guardar el empleado."
            )

    def seleccionar_empleado(self, event):
        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(seleccion[0], "values")

        self.id_empleado = valores[0]

        self.nombre.delete(0, "end")
        self.nombre.insert(0, valores[1])

        self.usuario.delete(0, "end")
        self.usuario.insert(0, valores[2])

        self.password.delete(0, "end")
        self.password.insert(0, valores[3])

        self.btn_guardar.configure(state="disabled")
        self.btn_modificar.configure(state="normal")
        self.btn_eliminar.configure(state="normal")

    def modificar(self):
        if self.id_empleado is None:
            return

        nombre = self.nombre.get().strip()
        usuario = self.usuario.get().strip()
        password = self.password.get().strip()

        if nombre == "" or usuario == "" or password == "":
            messagebox.showwarning(
                "Atención",
                "Debe completar nombre, usuario y contraseña."
            )
            return

        ok = actualizar_empleado(
            self.id_empleado,
            nombre,
            usuario,
            password
        )

        if ok:
            messagebox.showinfo(
                "Correcto",
                "Empleado actualizado correctamente."
            )

            self.nuevo()
            self.cargar_empleados()

        else:
            messagebox.showerror(
                "Error",
                "No fue posible actualizar el empleado."
            )

    def eliminar(self):
        if self.id_empleado is None:
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar este empleado?"
        )

        if not respuesta:
            return

        ok = eliminar_empleado(self.id_empleado)

        if ok:
            messagebox.showinfo(
                "Correcto",
                "Empleado eliminado correctamente."
            )

            self.nuevo()
            self.cargar_empleados()

        else:
            messagebox.showerror(
                "Error",
                "No fue posible eliminar el empleado."
            )