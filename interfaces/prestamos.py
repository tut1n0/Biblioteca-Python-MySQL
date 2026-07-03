import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import date

from controladores.prestamo_controller import (
    guardar_prestamo,
    obtener_prestamos,
    obtener_prestamos_activos,
    actualizar_prestamo,
    eliminar_prestamo
)

from controladores.socio_controller import obtener_socios_combo
from controladores.libro_controller import obtener_libros_combo
from controladores.empleado_controller import obtener_empleados_combo


class PrestamosFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.id_prestamo = None

        self.socios = {}
        self.empleados = {}
        self.libros = {}

        self.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            self,
            text="Gestión de Préstamos",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

        formulario = ctk.CTkFrame(self)
        formulario.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(formulario, text="Socio").grid(
            row=0, column=0, padx=10, pady=(15, 5), sticky="w"
        )

        self.combo_socio = ctk.CTkComboBox(
            formulario,
            width=220,
            state="readonly"
        )
        self.combo_socio.grid(row=1, column=0, padx=10, pady=5)

        ctk.CTkLabel(formulario, text="Empleado").grid(
            row=0, column=1, padx=10, pady=(15, 5), sticky="w"
        )

        self.combo_empleado = ctk.CTkComboBox(
            formulario,
            width=180,
            state="readonly"
        )
        self.combo_empleado.grid(row=1, column=1, padx=10, pady=5)

        ctk.CTkLabel(formulario, text="Libro").grid(
            row=0, column=2, padx=10, pady=(15, 5), sticky="w"
        )

        self.combo_libro = ctk.CTkComboBox(
            formulario,
            width=240,
            state="readonly"
        )
        self.combo_libro.grid(row=1, column=2, padx=10, pady=5)

        ctk.CTkLabel(formulario, text="Fecha préstamo").grid(
            row=2, column=0, padx=10, pady=(15, 5), sticky="w"
        )

        self.fecha_prestamo = ctk.CTkEntry(formulario, width=160)
        self.fecha_prestamo.grid(row=3, column=0, padx=10, pady=5)

        ctk.CTkLabel(formulario, text="Fecha devolución").grid(
            row=2, column=1, padx=10, pady=(15, 5), sticky="w"
        )

        self.fecha_devolucion = ctk.CTkEntry(formulario, width=160)
        self.fecha_devolucion.grid(row=3, column=1, padx=10, pady=5)

        ctk.CTkLabel(formulario, text="Estado").grid(
            row=2, column=2, padx=10, pady=(15, 5), sticky="w"
        )

        self.estado = ctk.CTkComboBox(
            formulario,
            values=["Prestado", "Devuelto"],
            width=160,
            state="readonly"
        )
        self.estado.grid(row=3, column=2, padx=10, pady=5)
        self.estado.set("Prestado")

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
                "socio",
                "empleado",
                "libro",
                "fecha_prestamo",
                "fecha_devolucion",
                "estado"
            ),
            show="headings",
            height=12
        )

        columnas = {
            "id": ("ID", 60),
            "socio": ("Socio", 170),
            "empleado": ("Empleado", 140),
            "libro": ("Libro", 220),
            "fecha_prestamo": ("Fecha préstamo", 130),
            "fecha_devolucion": ("Fecha devolución", 140),
            "estado": ("Estado", 100)
        }

        for columna, (texto, ancho) in columnas.items():
            self.tabla.heading(columna, text=texto)
            self.tabla.column(columna, width=ancho, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=20, pady=10)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_prestamo)

        self.cargar_combos()
        self.cargar_prestamos()
        self.nuevo()

    def cargar_combos(self):
        socios = obtener_socios_combo()
        self.socios.clear()

        nombres_socios = []

        for id_socio, nombre in socios:
            self.socios[nombre] = id_socio
            nombres_socios.append(nombre)

        self.combo_socio.configure(values=nombres_socios)

        if nombres_socios:
            self.combo_socio.set(nombres_socios[0])

        empleados = obtener_empleados_combo()
        self.empleados.clear()

        nombres_empleados = []

        for id_empleado, nombre in empleados:
            self.empleados[nombre] = id_empleado
            nombres_empleados.append(nombre)

        self.combo_empleado.configure(values=nombres_empleados)

        if nombres_empleados:
            self.combo_empleado.set(nombres_empleados[0])

        libros = obtener_libros_combo()
        self.libros.clear()

        titulos_libros = []

        for id_libro, titulo in libros:
            self.libros[titulo] = id_libro
            titulos_libros.append(titulo)

        self.combo_libro.configure(values=titulos_libros)

        if titulos_libros:
            self.combo_libro.set(titulos_libros[0])

    def cargar_prestamos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        prestamos = obtener_prestamos()

        for prestamo in prestamos:
            self.tabla.insert("", "end", values=prestamo)

    def nuevo(self):
        self.id_prestamo = None

        if self.combo_socio.cget("values"):
            self.combo_socio.set(self.combo_socio.cget("values")[0])

        if self.combo_empleado.cget("values"):
            self.combo_empleado.set(self.combo_empleado.cget("values")[0])

        if self.combo_libro.cget("values"):
            self.combo_libro.set(self.combo_libro.cget("values")[0])

        self.fecha_prestamo.delete(0, "end")
        self.fecha_prestamo.insert(0, date.today().strftime("%Y-%m-%d"))

        self.fecha_devolucion.delete(0, "end")

        self.estado.set("Prestado")

        self.btn_guardar.configure(state="normal")
        self.btn_modificar.configure(state="disabled")
        self.btn_eliminar.configure(state="disabled")

    def guardar(self):
        socio = self.combo_socio.get()
        empleado = self.combo_empleado.get()
        libro = self.combo_libro.get()

        id_socio = self.socios.get(socio)
        id_empleado = self.empleados.get(empleado)
        id_libro = self.libros.get(libro)

        fecha_prestamo = self.fecha_prestamo.get().strip()
        fecha_devolucion = self.fecha_devolucion.get().strip()
        estado = self.estado.get()

        if id_socio is None or id_empleado is None or id_libro is None:
            messagebox.showwarning(
                "Atención",
                "Debe seleccionar socio, empleado y libro."
            )
            return

        if fecha_prestamo == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar la fecha de préstamo."
            )
            return

        if fecha_devolucion == "":
            fecha_devolucion = None

        ok = guardar_prestamo(
            id_socio,
            id_empleado,
            id_libro,
            fecha_prestamo,
            fecha_devolucion,
            estado
        )

        if ok:
            messagebox.showinfo(
                "Correcto",
                "Préstamo guardado correctamente."
            )

            self.nuevo()
            self.cargar_prestamos()

        else:
            messagebox.showerror(
                "Error",
                "No fue posible guardar el préstamo."
            )

    def seleccionar_prestamo(self, event):
        seleccion = self.tabla.selection()

        if not seleccion:
            return

        valores = self.tabla.item(seleccion[0], "values")

        self.id_prestamo = valores[0]

        self.combo_socio.set(valores[1])
        self.combo_empleado.set(valores[2])
        self.combo_libro.set(valores[3])

        self.fecha_prestamo.delete(0, "end")
        self.fecha_prestamo.insert(0, valores[4])

        self.fecha_devolucion.delete(0, "end")
        if valores[5]:
            self.fecha_devolucion.insert(0, valores[5])

        self.estado.set(valores[6])

        self.btn_guardar.configure(state="disabled")
        self.btn_modificar.configure(state="normal")
        self.btn_eliminar.configure(state="normal")

    def modificar(self):
        if self.id_prestamo is None:
            return

        socio = self.combo_socio.get()
        empleado = self.combo_empleado.get()
        libro = self.combo_libro.get()

        id_socio = self.socios.get(socio)
        id_empleado = self.empleados.get(empleado)
        id_libro = self.libros.get(libro)

        fecha_prestamo = self.fecha_prestamo.get().strip()
        fecha_devolucion = self.fecha_devolucion.get().strip()
        estado = self.estado.get()

        if id_socio is None or id_empleado is None or id_libro is None:
            messagebox.showwarning(
                "Atención",
                "Debe seleccionar socio, empleado y libro."
            )
            return

        if fecha_prestamo == "":
            messagebox.showwarning(
                "Atención",
                "Debe ingresar la fecha de préstamo."
            )
            return

        if fecha_devolucion == "":
            fecha_devolucion = None

        ok = actualizar_prestamo(
            self.id_prestamo,
            id_socio,
            id_empleado,
            id_libro,
            fecha_prestamo,
            fecha_devolucion,
            estado
        )

        if ok:
            messagebox.showinfo(
                "Correcto",
                "Préstamo actualizado correctamente."
            )

            self.nuevo()
            self.cargar_prestamos()

        else:
            messagebox.showerror(
                "Error",
                "No fue posible actualizar el préstamo."
            )

    def eliminar(self):
        if self.id_prestamo is None:
            return

        respuesta = messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar este préstamo?"
        )

        if not respuesta:
            return

        ok = eliminar_prestamo(self.id_prestamo)

        if ok:
            messagebox.showinfo(
                "Correcto",
                "Préstamo eliminado correctamente."
            )

            self.nuevo()
            self.cargar_prestamos()

        else:
            messagebox.showerror(
                "Error",
                "No fue posible eliminar el préstamo."
            )


class PrestamosCirculacionFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            self,
            text="Préstamos en Circulación",
            font=("Arial", 24, "bold")
        ).pack(pady=15)

        self.tabla = ttk.Treeview(
            self,
            columns=(
                "id",
                "socio",
                "libro",
                "fecha_prestamo",
                "fecha_devolucion"
            ),
            show="headings",
            height=16
        )

        columnas = {
            "id": ("ID", 60),
            "socio": ("Socio", 220),
            "libro": ("Libro", 260),
            "fecha_prestamo": ("Fecha préstamo", 140),
            "fecha_devolucion": ("Fecha devolución", 140)
        }

        for columna, (texto, ancho) in columnas.items():
            self.tabla.heading(columna, text=texto)
            self.tabla.column(columna, width=ancho, anchor="center")

        self.tabla.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_prestamos_activos()

    def cargar_prestamos_activos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        prestamos = obtener_prestamos_activos()

        for prestamo in prestamos:
            self.tabla.insert("", "end", values=prestamo)
