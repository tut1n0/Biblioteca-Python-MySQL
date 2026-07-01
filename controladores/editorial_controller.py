from conexion import conectar


def guardar_editorial(nombre):

    conexion = conectar()

    if conexion is None:
        return False

    try:

        cursor = conexion.cursor()

        sql = """
        INSERT INTO editoriales
        (nombre)
        VALUES (%s)
        """

        cursor.execute(
            sql,
            (nombre,)
        )

        conexion.commit()

        return True

    except Exception as e:

        print("Error al guardar editorial:", e)
        return False

    finally:

        cursor.close()
        conexion.close()


def obtener_editoriales():

    conexion = conectar()

    if conexion is None:
        return []

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_editorial,
                nombre
            FROM editoriales
            ORDER BY nombre
        """)

        return cursor.fetchall()

    except Exception as e:

        print("Error:", e)
        return []

    finally:

        cursor.close()
        conexion.close()


def actualizar_editorial(id_editorial, nombre):

    conexion = conectar()

    if conexion is None:
        return False

    try:

        cursor = conexion.cursor()

        sql = """
        UPDATE editoriales
        SET nombre=%s
        WHERE id_editorial=%s
        """

        cursor.execute(
            sql,
            (
                nombre,
                id_editorial
            )
        )

        conexion.commit()

        return True

    except Exception as e:

        print("Error al actualizar:", e)
        return False

    finally:

        cursor.close()
        conexion.close()


def eliminar_editorial(id_editorial):

    conexion = conectar()

    if conexion is None:
        return False

    try:

        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM editoriales WHERE id_editorial=%s",
            (id_editorial,)
        )

        conexion.commit()

        return True

    except Exception as e:

        print("Error al eliminar:", e)
        return False

    finally:

        cursor.close()
        conexion.close()