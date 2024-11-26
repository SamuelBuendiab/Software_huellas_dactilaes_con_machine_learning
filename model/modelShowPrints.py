import sqlite3

from model.dbConnetion import conectar  # Asegúrate de que la conexión está importada correctamente
class ModeloHuellas:
    def __init__(self):
        self.conexion = conectar()
        if self.conexion is None:
            raise Exception("No se pudo establecer la conexión con la base de datos.")

    def obtener_huellas_usuario(self, user_id):
        self.conexion.row_factory = sqlite3.Row  # Configurar para devolver filas como diccionarios
        cursor = self.conexion.cursor()
        query = "SELECT idhuella, iduser, mano, tipo_dedo, tipo_huella, resultado_analisis, imagen_path FROM huellas WHERE iduser = ?"
        cursor.execute(query, (user_id,))
        huellas = cursor.fetchall()
        cursor.close()

        # Depurar los resultados
        print(f"Resultado de la consulta: {huellas}")
        return huellas

    def obtener_calculos_usuario(self, user_id):
        self.conexion.row_factory = sqlite3.Row  # Configurar para devolver filas como diccionarios
        cursor = self.conexion.cursor()
        # Consulta para obtener los resultados de cálculos
        query_calculos = """
            SELECT d10, sctlmd, sctlmi, sctl, campo_a, campo_l, campo_w, diseño, comentario
            FROM resultados_calculos
            WHERE iduser = ?
            """
        cursor.execute(query_calculos, (user_id,))
        calculos = cursor.fetchone()  # Traer solo un resultado porque debería ser único para cada usuario

        # Depurar los resultados
        print(f"Resultado de la consulta: {calculos}")
        return calculos




