from conexion import conectar


def guardar_socio(nombre, apellido, dni, telefono, email, direccion):
    conexion = conectar()

    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()

        sql = """
        INSERT INTO socios
        (nombre, apellido, dni, telefono, email, direccion)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (nombre, apellido, dni, telefono, email, direccion))
        conexion.commit()

        return True

    except Exception as e:
        print("Error al guardar socio:", e)
        return False

    finally:
        cursor.close()
        conexion.close()


def obtener_socios():
    conexion = conectar()

    if conexion is None:
        return []

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_socio,
                nombre,
                apellido,
                dni,
                telefono,
                email,
                direccion
            FROM socios
            ORDER BY apellido, nombre
        """)

        return cursor.fetchall()

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        conexion.close()


def actualizar_socio(id_socio, nombre, apellido, dni, telefono, email, direccion):
    conexion = conectar()

    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()

        sql = """
        UPDATE socios
        SET
            nombre=%s,
            apellido=%s,
            dni=%s,
            telefono=%s,
            email=%s,
            direccion=%s
        WHERE id_socio=%s
        """

        cursor.execute(
            sql,
            (nombre, apellido, dni, telefono, email, direccion, id_socio)
        )

        conexion.commit()

        return True

    except Exception as e:
        print("Error al actualizar socio:", e)
        return False

    finally:
        cursor.close()
        conexion.close()


def eliminar_socio(id_socio):
    conexion = conectar()

    if conexion is None:
        return False

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM socios WHERE id_socio=%s",
            (id_socio,)
        )

        conexion.commit()

        return True

    except Exception as e:
        print("Error al eliminar socio:", e)
        return False

    finally:
        cursor.close()
        conexion.close()
def obtener_socios_combo():
    conexion = conectar()

    if conexion is None:
        return []

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_socio,
                CONCAT(nombre, ' ', apellido) AS socio
            FROM socios
            ORDER BY apellido, nombre
        """)

        return cursor.fetchall()

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        conexion.close()