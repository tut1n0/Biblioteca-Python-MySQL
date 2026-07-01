from conexion import conectar


def guardar_autor(nombre, nacionalidad):

    conexion = conectar()

    if conexion is None:
        return False

    try:

        cursor = conexion.cursor()

        sql = """
        INSERT INTO autores
        (nombre, nacionalidad)
        VALUES (%s, %s)
        """

        cursor.execute(
            sql,
            (
                nombre,
                nacionalidad
            )
        )

        conexion.commit()

        return True

    except Exception as e:

        print("Error al guardar autor:", e)
        return False

    finally:

        cursor.close()
        conexion.close()


def obtener_autores():

    conexion = conectar()

    if conexion is None:
        return []

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_autor,
                nombre,
                nacionalidad
            FROM autores
            ORDER BY nombre
        """)

        return cursor.fetchall()

    except Exception as e:

        print("Error:", e)
        return []

    finally:

        cursor.close()
        conexion.close()


def actualizar_autor(id_autor, nombre, nacionalidad):

    conexion = conectar()

    if conexion is None:
        return False

    try:

        cursor = conexion.cursor()

        sql = """
        UPDATE autores
        SET
            nombre=%s,
            nacionalidad=%s
        WHERE id_autor=%s
        """

        cursor.execute(
            sql,
            (
                nombre,
                nacionalidad,
                id_autor
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


def eliminar_autor(id_autor):

    conexion = conectar()

    if conexion is None:
        return False

    try:

        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM autores WHERE id_autor=%s",
            (id_autor,)
        )

        conexion.commit()

        return True

    except Exception as e:

        print("Error al eliminar:", e)
        return False

    finally:

        cursor.close()
        conexion.close()
        
def obtener_autores_combo():

    conexion = conectar()

    if conexion is None:
        return []

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_autor,
                nombre
            FROM autores
            ORDER BY nombre
        """)

        return cursor.fetchall()

    except Exception as e:

        print("Error:", e)
        return []

    finally:

        cursor.close()
        conexion.close()