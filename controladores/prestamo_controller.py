from conexion import conectar


def obtener_stock_libro(cursor, id_libro):
    cursor.execute(
        "SELECT stock FROM libros WHERE id_libro=%s",
        (id_libro,)
    )

    resultado = cursor.fetchone()

    if resultado is None:
        return None

    return resultado[0]


def bajar_stock(cursor, id_libro):
    stock = obtener_stock_libro(cursor, id_libro)

    if stock is None:
        return False

    if stock <= 0:
        return False

    cursor.execute(
        "UPDATE libros SET stock = stock - 1 WHERE id_libro=%s",
        (id_libro,)
    )

    return True


def subir_stock(cursor, id_libro):
    cursor.execute(
        "UPDATE libros SET stock = stock + 1 WHERE id_libro=%s",
        (id_libro,)
    )


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

        if estado == "Prestado":
            if not bajar_stock(cursor, id_libro):
                print("No hay stock disponible para este libro.")
                return False

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
        conexion.rollback()
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


def obtener_prestamos_activos():
    conexion = conectar()

    if conexion is None:
        return []

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                p.id_prestamo,
                CONCAT(s.nombre, ' ', s.apellido) AS socio,
                l.titulo AS libro,
                p.fecha_prestamo,
                p.fecha_devolucion
            FROM prestamos p

            LEFT JOIN socios s
                ON p.id_socio = s.id_socio

            LEFT JOIN libros l
                ON p.id_libro = l.id_libro

            WHERE p.estado = 'Prestado'
            ORDER BY p.fecha_prestamo DESC
        """)

        return cursor.fetchall()

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        conexion.close()


def obtener_prestamo_por_id(cursor, id_prestamo):
    cursor.execute("""
        SELECT
            id_libro,
            estado
        FROM prestamos
        WHERE id_prestamo=%s
    """, (id_prestamo,))

    return cursor.fetchone()


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

        cursor.execute("""
            SELECT id_libro, estado
            FROM prestamos
            WHERE id_prestamo=%s
        """, (id_prestamo,))

        prestamo_actual = cursor.fetchone()

        if prestamo_actual is None:
            return False

        id_libro_anterior = prestamo_actual[0]
        estado_anterior = str(prestamo_actual[1]).strip()
        estado_nuevo = str(estado).strip()

        print("DEBUG PRESTAMO")
        print("ID:", id_prestamo)
        print("Libro anterior:", id_libro_anterior)
        print("Libro nuevo:", id_libro)
        print("Estado anterior:", estado_anterior)
        print("Estado nuevo:", estado_nuevo)

        if estado_anterior == "Prestado" and estado_nuevo == "Devuelto":
            cursor.execute(
                "UPDATE libros SET stock = stock + 1 WHERE id_libro=%s",
                (id_libro_anterior,)
            )
            print("Stock aumentado para libro:", id_libro_anterior)

        elif estado_anterior == "Devuelto" and estado_nuevo == "Prestado":
            if not bajar_stock(cursor, id_libro):
                print("No hay stock disponible.")
                return False

        elif estado_anterior == "Prestado" and estado_nuevo == "Prestado":
            if str(id_libro_anterior) != str(id_libro):
                cursor.execute(
                    "UPDATE libros SET stock = stock + 1 WHERE id_libro=%s",
                    (id_libro_anterior,)
                )

                if not bajar_stock(cursor, id_libro):
                    cursor.execute(
                        "UPDATE libros SET stock = stock - 1 WHERE id_libro=%s",
                        (id_libro_anterior,)
                    )
                    print("No hay stock disponible para el nuevo libro.")
                    return False

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
                estado_nuevo,
                id_prestamo
            )
        )

        conexion.commit()
        return True

    except Exception as e:
        conexion.rollback()
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

        prestamo_actual = obtener_prestamo_por_id(cursor, id_prestamo)

        if prestamo_actual is None:
            return False

        id_libro = prestamo_actual[0]
        estado = prestamo_actual[1]

        if estado == "Prestado":
            subir_stock(cursor, id_libro)

        cursor.execute(
            "DELETE FROM prestamos WHERE id_prestamo=%s",
            (id_prestamo,)
        )

        conexion.commit()

        return True

    except Exception as e:
        conexion.rollback()
        print("Error al eliminar préstamo:", e)
        return False

    finally:
        cursor.close()
        conexion.close()