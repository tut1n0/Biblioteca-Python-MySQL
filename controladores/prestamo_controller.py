from conexion import conectar


def guardar_prestamo(
    id_socio,
    id_empleado,
    id_libro,
    fecha_prestamo,
    fecha_devolucion,
    estado
):
    conexion = conectar()

    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()

        sql = """
        INSERT INTO prestamos
        (
            id_socio,
            id_empleado,
            id_libro,
            fecha_prestamo,
            fecha_devolucion,
            estado
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                id_socio,
                id_empleado,
                id_libro,
                fecha_prestamo,
                fecha_devolucion,
                estado
            )
        )

        conexion.commit()

        return True

    except Exception as e:
        print("Error al guardar préstamo:", e)
        return False

    finally:
        cursor.close()
        conexion.close()


def obtener_prestamos():
    conexion = conectar()

    if conexion is None:
        return []

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                p.id_prestamo,
                CONCAT(s.nombre, ' ', s.apellido) AS socio,
                e.nombre AS empleado,
                l.titulo AS libro,
                p.fecha_prestamo,
                p.fecha_devolucion,
                p.estado
            FROM prestamos p

            LEFT JOIN socios s
                ON p.id_socio = s.id_socio

            LEFT JOIN empleados e
                ON p.id_empleado = e.id_empleado

            LEFT JOIN libros l
                ON p.id_libro = l.id_libro

            ORDER BY p.fecha_prestamo DESC
        """)

        return cursor.fetchall()

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        conexion.close()


def actualizar_prestamo(
    id_prestamo,
    id_socio,
    id_empleado,
    id_libro,
    fecha_prestamo,
    fecha_devolucion,
    estado
):
    conexion = conectar()

    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()

        sql = """
        UPDATE prestamos
        SET
            id_socio=%s,
            id_empleado=%s,
            id_libro=%s,
            fecha_prestamo=%s,
            fecha_devolucion=%s,
            estado=%s
        WHERE id_prestamo=%s
        """

        cursor.execute(
            sql,
            (
                id_socio,
                id_empleado,
                id_libro,
                fecha_prestamo,
                fecha_devolucion,
                estado,
                id_prestamo
            )
        )

        conexion.commit()

        return True

    except Exception as e:
        print("Error al actualizar préstamo:", e)
        return False

    finally:
        cursor.close()
        conexion.close()


def eliminar_prestamo(id_prestamo):
    conexion = conectar()

    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM prestamos WHERE id_prestamo=%s",
            (id_prestamo,)
        )

        conexion.commit()

        return True

    except Exception as e:
        print("Error al eliminar préstamo:", e)
        return False

    finally:
        cursor.close()
        conexion.close()