import pymysql
from config import *

def conectar():
    try:
        print("Intentando conectar...")

        conexion = pymysql.connect(
            host=HOST,
            user=USUARIO,
            password=PASSWORD,
            database=DATABASE,
            port=PUERTO,
            connect_timeout=5
        )

        print("✅ Conexión exitosa")
        return conexion

    except Exception as e:
        print("❌ Error de conexión:", e)
        return None