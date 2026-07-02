from conexion import conectar


def guardar_empleado(nombre, usuario, password):
    conexion = conectar()

    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO empleados
            (nombre, usuario, password)
            VALUES (%s, %s, %s)
        """, (nombre, usuario, password))

        conexion.commit()
        return True

    except Exception as e:
        print("Error al guardar empleado:", e)
        return False

    finally:
        cursor.close()
        conexion.close()


def obtener_empleados():
    conexion = conectar()

    if conexion is None:
        return []

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_empleado,
                nombre,
                usuario,
                password
            FROM empleados
            ORDER BY nombre
        """)

        return cursor.fetchall()

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        conexion.close()


def actualizar_empleado(id_empleado, nombre, usuario, password):
    conexion = conectar()

    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            UPDATE empleados
            SET
                nombre=%s,
                usuario=%s,
                password=%s
            WHERE id_empleado=%s
        """, (nombre, usuario, password, id_empleado))

        conexion.commit()
        return True

    except Exception as e:
        print("Error al actualizar empleado:", e)
        return False

    finally:
        cursor.close()
        conexion.close()


def eliminar_empleado(id_empleado):
    conexion = conectar()

    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM empleados WHERE id_empleado=%s",
            (id_empleado,)
        )

        conexion.commit()
        return True

    except Exception as e:
        print("Error al eliminar empleado:", e)
        return False

    finally:
        cursor.close()
        conexion.close()


def obtener_empleados_combo():
    conexion = conectar()

    if conexion is None:
        return []

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_empleado,
                nombre
            FROM empleados
            ORDER BY nombre
        """)

        return cursor.fetchall()

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        conexion.close()