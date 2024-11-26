import sqlite3

from model.dbConnetion import conectar
import textwrap
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas


class ModeloUsuario:
    def __init__(self):
        self.conexion = conectar()


    def agregar_usuario(self, nombre, grupo, correo, numero_id, numero_celular, edad, genero, idhuellas=None):
        cursor = self.conexion.cursor()
        try:
            # Convertir genero a mayúsculas
            genero = genero.upper()

            query = """INSERT INTO user (name, grupo, correo, numero_id, numero_celular, edad, genero) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, (nombre, grupo, correo, numero_id, numero_celular, edad, genero))
            self.conexion.commit()

            user_id = cursor.lastrowid
            print(f"Usuario agregado exitosamente con ID: {user_id}")
            return user_id

        except sqlite3.Error as err:
            print(f"Error al agregar usuario: {err}")
            return None
        finally:
            cursor.close()

    def obtener_usuarios(self):
        cursor = self.conexion.cursor()

        # Ahora incluye el iduser en la consulta para que lo puedas usar
       # cursor.execute("SELECT iduser, name, correo, numero_id, numero_celular FROM user")
        cursor.execute("SELECT iduser, name, grupo, correo, numero_id, numero_celular, edad, genero,fecha_hora_insercion FROM user")

        usuarios = cursor.fetchall()
        cursor.close()
        return usuarios

    def eliminar_usuario(self, user_id):
        cursor = self.conexion.cursor()
        try:
            cursor.execute("DELETE FROM user WHERE iduser = ?", (user_id,))
            self.conexion.commit()
        except sqlite3.Error as err:
            print(f"Error al eliminar usuario: {err}")
        finally:
            cursor.close()

    def actualizar_usuario(self, user_id, nombre,grupo, correo, numero_id, numero_celular, edad, genero):
        cursor = self.conexion.cursor()
        try:
            cursor.execute("""UPDATE user 
                              SET name = ?, grupo = ?, correo = ?, numero_id = ?, numero_celular = ?, edad = ?, genero = ?
                              WHERE iduser = ?""",
                           (nombre, grupo,correo, numero_id, numero_celular, edad, genero, user_id))
            self.conexion.commit()
            print("Usuario actualizado exitosamente.")
            return True
        except sqlite3.Error as err:
            print(f"Error al actualizar usuario: {err}")
            return False
        finally:
            cursor.close()

    def generar_reporte(self, fecha_inicio, fecha_fin=None, archivo_destino="reporte_usuario.pdf"):
        cursor = self.conexion.cursor()

        # Crear el archivo PDF en orientación horizontal (más ancho)
        c = canvas.Canvas(archivo_destino, pagesize=landscape(letter))

        # Título del reporte
        c.setFont("Helvetica-Bold", 16)
        c.drawString(250, 550, "Reporte de Usuarios")

        # Consulta SQL para obtener los datos dentro del rango de fechas
        if fecha_fin:
            query = """
                SELECT name, correo, numero_id, numero_celular, edad, genero, fecha_hora_insercion
                FROM user
                WHERE fecha_hora_insercion BETWEEN ? AND ?
            """
            cursor.execute(query, (fecha_inicio, fecha_fin))
        else:
            query = """
                SELECT name, correo, numero_id, numero_celular, edad, genero, fecha_hora_insercion
                FROM user
                WHERE fecha_hora_insercion >= ?
            """
            cursor.execute(query, (fecha_inicio,))

        # Obtener los resultados
        rows = cursor.fetchall()

        # Configurar el formato de los datos
        y_position = 500  # Posición en el eje Y para los datos en el PDF
        c.setFont("Helvetica-Bold", 10)

        # Escribir los encabezados
        headers = ["Nombre", "Correo", "Número de ID", "Número\nCelular", "Edad", "Género", "Fecha y hora"]
        column_widths = [50, 150, 300, 400, 470, 520, 600]  # Ajuste de espacios para columnas

        for i, header in enumerate(headers):
            # Si el header contiene "\n", dibujarlo en dos líneas
            if "\n" in header:
                line1, line2 = header.split("\n")
                c.drawString(column_widths[i], y_position, line1)
                c.drawString(column_widths[i], y_position - 10, line2)  # Coloca la segunda línea un poco más abajo
            else:
                c.drawString(column_widths[i], y_position, header)

        y_position -= 30  # Espacio para las filas de datos

        # Ajuste del espaciado entre filas
        c.setFont("Helvetica", 9)

        # Función para dividir texto en varias líneas si es necesario
        def ajustar_texto(c, text, x, y, width, max_line_length=25):
            if len(text) > max_line_length:
                # Divide el texto en varias líneas si es más largo que el máximo
                for line in textwrap.wrap(text, max_line_length):
                    c.drawString(x, y, line)
                    y -= 10  # Espacio entre líneas
            else:
                c.drawString(x, y, text)

        # Escribir los datos de los usuarios
        for row in rows:
            for i, data in enumerate(row):
                x_position = column_widths[i]
                if i == 1:  # Si es la columna de correo, permite ajuste de texto en varias líneas
                    ajustar_texto(c, str(data), x_position, y_position, 100, max_line_length=30)
                else:
                    c.drawString(x_position, y_position, str(data))
            y_position -= 25  # Aumentar el espacio entre filas

        # Guardar el PDF
        c.save()
        cursor.close()

        print(f"Reporte generado en: {archivo_destino}")




