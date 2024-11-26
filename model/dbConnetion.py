import sqlite3
import os

DB_NAME = "proyecto_prueba.sqlite"  # Archivo de base de datos SQLite

def conectar():
    """Función para conectar a la base de datos SQLite."""
    try:
        # Conexión a la base de datos SQLite (crea el archivo si no existe)
        conexion = sqlite3.connect(DB_NAME)
        print(f"Conexión exitosa a la base de datos '{DB_NAME}'.")
        return conexion
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None



def initialize_database():
    """Inicializa la base de datos SQLite y crea las tablas si no existen."""
    try:
        conexion = conectar()
        if not conexion:
            print("No se pudo conectar a la base de datos.")
            return

        cursor = conexion.cursor()

        # Crear la tabla 'user' si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            iduser INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grupo TEXT NOT NULL,
            correo TEXT NOT NULL,
            numero_id INTEGER NOT NULL,
            numero_celular TEXT DEFAULT NULL,
            edad INTEGER DEFAULT NULL,
            genero TEXT DEFAULT NULL,
            fecha_hora_insercion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Crear la tabla 'huellas' si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS huellas (
            idhuella INTEGER PRIMARY KEY AUTOINCREMENT,
            iduser INTEGER NOT NULL,
            mano TEXT DEFAULT NULL,
            tipo_dedo TEXT DEFAULT NULL,
            tipo_huella TEXT CHECK(tipo_huella IN ('verticilo', 'presilla', 'arco')) NOT NULL,
            resultado_analisis INTEGER DEFAULT NULL,
            imagen_path TEXT NOT NULL,
            FOREIGN KEY (iduser) REFERENCES user (iduser) ON DELETE CASCADE
        )
        """)

        # Crear la tabla 'registro' si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS registro (
            idregistro INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            contraseña TEXT NOT NULL
        )
        """)

        # Crear la tabla 'resultados_calculos' si no existe
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS resultados_calculos (
            id_resultados INTEGER PRIMARY KEY AUTOINCREMENT,
            iduser INTEGER NOT NULL,
            d10 INTEGER DEFAULT NULL,
            sctlmd INTEGER DEFAULT NULL,
            sctlmi INTEGER DEFAULT NULL,
            sctl INTEGER DEFAULT NULL,
            campo_a INTEGER DEFAULT NULL,
            campo_l INTEGER DEFAULT NULL,
            campo_w INTEGER DEFAULT NULL,
            diseño TEXT,
            comentario TEXT,
            FOREIGN KEY (iduser) REFERENCES user (iduser) ON DELETE CASCADE
        )
        """)

        conexion.commit()
        print("Base de datos y tablas creadas o verificadas correctamente.")
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        if conexion:
            conexion.close()
