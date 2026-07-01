from conexion import conectar


def guardar_categoria(nombre):

    conexion = conectar()

    if conexion is None:
        return False

    try:

        cursor = conexion.cursor()

        sql = """
        INSERT INTO categorias
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

        print("Error al guardar categoria:", e)
        return False

    finally:

        cursor.close()
        conexion.close()


def obtener_categorias():

    conexion = conectar()

    if conexion is None:
        return []

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_categoria,
                nombre
            FROM categorias
            ORDER BY nombre
        """)

        return cursor.fetchall()

    except Exception as e:

        print("Error:", e)
        return []

    finally:

        cursor.close()
        conexion.close()


def actualizar_categoria(id_categoria, nombre):

    conexion = conectar()

    if conexion is None:
        return False

    try:

        cursor = conexion.cursor()

        sql = """
        UPDATE categorias
        SET nombre=%s
        WHERE id_categoria=%s
        """

        cursor.execute(
            sql,
            (
                nombre,
                id_categoria
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


def eliminar_categoria(id_categoria):

    conexion = conectar()

    if conexion is None:
        return False

    try:

        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM categorias WHERE id_categoria=%s",
            (id_categoria,)
        )

        conexion.commit()

        return True

    except Exception as e:

        print("Error al eliminar:", e)
        return False

    finally:

        cursor.close()
        conexion.close()