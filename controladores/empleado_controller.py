from conexion import conectar


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