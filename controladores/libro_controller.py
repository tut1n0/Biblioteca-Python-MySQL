from conexion import conectar


def guardar_libro(
    titulo,
    isbn,
    anio,
    stock,
    id_autor,
    id_editorial,
    id_categoria
):

    conexion = conectar()

    if conexion is None:
        return False

    try:

        cursor = conexion.cursor()

        sql = """
        INSERT INTO libros
        (
            titulo,
            isbn,
            anio_publicacion,
            stock,
            id_autor,
            id_editorial,
            id_categoria
        )
        VALUES
        (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            sql,
            (
                titulo,
                isbn,
                anio,
                stock,
                id_autor,
                id_editorial,
                id_categoria
            )
        )

        conexion.commit()

        return True

    except Exception as e:

        print("Error al guardar:", e)
        return False

    finally:

        cursor.close()
        conexion.close()


def obtener_libros():

    conexion = conectar()

    if conexion is None:
        return []

    try:

        cursor = conexion.cursor()

        cursor.execute("""
            SELECT

                l.id_libro,
                l.titulo,
                l.isbn,
                l.anio_publicacion,
                l.stock,

                a.nombre AS autor,
                e.nombre AS editorial,
                c.nombre AS categoria

            FROM libros l

            LEFT JOIN autores a
                ON l.id_autor = a.id_autor

            LEFT JOIN editoriales e
                ON l.id_editorial = e.id_editorial

            LEFT JOIN categorias c
                ON l.id_categoria = c.id_categoria

            ORDER BY l.titulo
        """)

        return cursor.fetchall()

    except Exception as e:

        print("Error:", e)
        return []

    finally:

        cursor.close()
        conexion.close()


def actualizar_libro(
    id_libro,
    titulo,
    isbn,
    anio,
    stock,
    id_autor,
    id_editorial,
    id_categoria
):

    conexion = conectar()

    if conexion is None:
        return False

    try:

        cursor = conexion.cursor()

        sql = """
        UPDATE libros
        SET
            titulo=%s,
            isbn=%s,
            anio_publicacion=%s,
            stock=%s,
            id_autor=%s,
            id_editorial=%s,
            id_categoria=%s
        WHERE id_libro=%s
        """

        cursor.execute(
            sql,
            (
                titulo,
                isbn,
                anio,
                stock,
                id_autor,
                id_editorial,
                id_categoria,
                id_libro
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


def eliminar_libro(id_libro):

    conexion = conectar()

    if conexion is None:
        return False

    try:

        cursor = conexion.cursor()

        cursor.execute(
            "DELETE FROM libros WHERE id_libro=%s",
            (id_libro,)
        )

        conexion.commit()

        return True

    except Exception as e:

        print("Error al eliminar:", e)
        return False

    finally:

        cursor.close()
        conexion.close()

def obtener_libros_combo():
    conexion = conectar()

    if conexion is None:
        return []

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT
                id_libro,
                titulo
            FROM libros
            ORDER BY titulo
        """)

        return cursor.fetchall()

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        conexion.close()