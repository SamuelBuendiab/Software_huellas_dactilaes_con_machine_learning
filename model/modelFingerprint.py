import os
from model.modelUser import ModeloUsuario  # Para obtener la información del usuario
from model.dbConnetion import conectar# Tu conexión a la base de datos
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image
import openpyxl

class ModeloHuellas:
    def __init__(self):
        self.conexion = conectar()
        self.modelo_usuario = ModeloUsuario()  # Instancia para obtener el usuario

    def crear_directorio_usuario(self, user_id, user_name):
        # Crear directorio basado en ID y nombre del usuario
        base_dir = "images"
        user_dir = f"{user_id}_{user_name}"
        path = os.path.join(base_dir, user_dir)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def guardar_imagen(self, user_id, user_name, imagen_path, dedo):
        # Guardar la imagen en el directorio del usuario
        user_dir = self.crear_directorio_usuario(user_id, user_name)
        imagen_destino = os.path.join(user_dir, f"{dedo}.png")  # Guardar con el nombre del dedo
        with open(imagen_path, 'rb') as src, open(imagen_destino, 'wb') as dst:
            dst.write(src.read())
        return imagen_destino

    def calcular_campos(self, user_id, comentario):
        conexion = conectar()
        if not conexion:
            print("No se pudo conectar a la base de datos.")
            return None

        try:
            cursor = conexion.cursor()
            query = "SELECT tipo_huella, resultado_analisis, mano FROM huellas WHERE iduser = ?"
            cursor.execute(query, (user_id,))
            huellas = cursor.fetchall()

            # Inicializar los contadores y acumuladores
            presillas = verticilos = arcos = 0
            sctlmd = sctlmi = 0

            for huella in huellas:
                tipo_huella = huella[0]  # primer campo: tipo_huella
                resultado_analisis = huella[1]  # segundo campo: resultado_analisis
                mano = huella[2]  # tercer campo: mano

                # Contar tipos de huella
                if tipo_huella == "presilla":
                    presillas += 1
                elif tipo_huella == "verticilo":
                    verticilos += 1
                elif tipo_huella == "arco":
                    arcos += 1

                # Sumar resultado_analisis según la mano
                if mano == "Derecho" and (tipo_huella == "verticilo" or tipo_huella == "presilla"):
                    sctlmd += resultado_analisis
                elif mano == "Izquierdo" and (tipo_huella == "verticilo" or tipo_huella == "presilla"):
                    sctlmi += resultado_analisis

            # Calcular los campos derivados
            d10 = presillas + (verticilos * 2)
            sctl = sctlmd + sctlmi
            campo_a = arcos
            campo_l = presillas
            campo_w = verticilos

            # Determinar diseño
            valores = {'L': campo_l, 'W': campo_w, 'A': campo_a}
            diseño = ''.join(sorted(valores, key=valores.get, reverse=True)[:2])

            # Preparar los valores para la inserción
            resultado = {
                'd10': d10,
                'sctlmd': sctlmd or 0,
                'sctlmi': sctlmi or 0,
                'sctl': sctl or 0,
                'campo_a': campo_a or 0,
                'campo_l': campo_l or 0,
                'campo_w': campo_w or 0,
                'diseño': diseño,
                'comentario':comentario
            }

            # Insertar los resultados en la tabla resultados_calculos
            insert_query = '''
                INSERT INTO resultados_calculos (iduser, d10, sctlmd, sctlmi, sctl, campo_a, campo_l, campo_w, diseño, comentario)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            parametros = (
                user_id,
                resultado['d10'],
                resultado['sctlmd'],
                resultado['sctlmi'],
                resultado['sctl'],
                resultado['campo_a'],
                resultado['campo_l'],
                resultado['campo_w'],
                resultado['diseño'],
                resultado['comentario']
            )

            cursor.execute(insert_query, parametros)
            conexion.commit()
            print("Resultados calculados y guardados en la base de datos correctamente.")

            return resultado

        except Exception as e:
            print(f"Error al calcular o guardar los resultados: {e}")
            conexion.rollback()
            return None

        finally:
            cursor.close()
            conexion.close()

    def guardar_comentario_bd(self, id_usuario, comentario):
        conexion = conectar()  # Conectar a la base de datos
        if conexion:
            try:
                cursor = conexion.cursor()
                consulta = '''
                INSERT INTO resultados_calculos (iduser, comentario)
                VALUES (?, ?)
                '''
                parametros = (id_usuario, comentario)
                cursor.execute(consulta, parametros)  # Cambiado a cursor.execute
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al insertar comentario en la base de datos: {e}")
                conexion.rollback()  # Hacer rollback si hay un error
                return False
            finally:
                cursor.close()
                conexion.close()
        else:
            print("No se pudo conectar a la base de datos.")
            return False

    def guardar_huella_en_bd(self, user_id, tipo_huella, resultado_analisis, imagen_path, mano, tipo_dedo):

        conexion = conectar()  # Conectar a la base de datos
        if conexion:
            try:
                cursor = conexion.cursor()
                query = """
                       INSERT INTO huellas (iduser, mano, tipo_dedo, tipo_huella, resultado_analisis, imagen_path)
                       VALUES (?, ?, ?, ?, ?, ?)
                       """
                valores = (user_id, mano, tipo_dedo, tipo_huella, resultado_analisis, imagen_path)
                cursor.execute(query, valores)
                conexion.commit()
                return True
            except Exception as e:
                print(f"Error al insertar en la base de datos: {e}")
                conexion.rollback()  # Hacer rollback si hay un error
                return False
            finally:
                cursor.close()
                conexion.close()
        else:
            print("No se pudo conectar a la base de datos.")
            return False

    def obtener_huellas_usuario(self, user_id):
        cursor = self.conexion.cursor(dictionary=True)
        query = "SELECT idhuella, iduser, tipo_huella, resultado_analisis, imagen_path FROM proyetogrado.huellas WHERE iduser = ?"
        cursor.execute(query, (user_id,))
        huellas = cursor.fetchall()
        cursor.close()
        return huellas

    def exportar_a_excel(self, archivo,grupo):
        cursor = self.conexion.cursor()

        try:
            query_usuarios = """
                    SELECT iduser, numero_id, edad, grupo
                    FROM user
                    WHERE grupo = ?
                """
            cursor.execute(query_usuarios, (grupo,))
            usuarios = cursor.fetchall()

            # Verificar si hay usuarios en el grupo
            if not usuarios:
                messagebox.showwarning("Advertencia", f"No hay usuarios en el grupo '{grupo}' para exportar.")
                return False

            datos_exportacion = []
            # Nombres de dedos esperados en el orden correcto
            nombres_dedos = [
                "Pulgar Derecho", "Indice Derecho", "Medio Derecho", "Anular Derecho", "Menique Derecho",
                "Pulgar Izquierdo", "Indice Izquierdo", "Medio Izquierdo", "Anular Izquierdo", "Menique Izquierdo"
            ]

            # Normalizamos nombres de dedos para que coincidan con el formato en la base de datos
            nombres_dedos_map = {dedo.lower(): dedo for dedo in nombres_dedos}

            # Listas para acumular los valores de campo_a, campo_l, y campo_w para la gráfica
            lista_campo_a = []
            lista_campo_l = []
            lista_campo_w = []

            for usuario in usuarios:
                iduser, numero_id, edad, grupo = usuario

                # Obtener datos de la tabla resultados_calculos
                query_resultados = """
                       SELECT d10, sctlmd, sctlmi, sctl, campo_a, campo_l, campo_w, diseño
                       FROM resultados_calculos
                       WHERE iduser = ?
                   """
                cursor.execute(query_resultados, (iduser,))
                resultados_calculos = cursor.fetchone()

                if resultados_calculos:
                    d10, sctlmd, sctlmi, sctl_total, campo_a, campo_l, campo_w, diseño = resultados_calculos
                else:
                    d10 = sctlmd = sctlmi = sctl_total = campo_a = campo_l = campo_w = diseño = 0

                # Añadir los valores de campo_a, campo_l y campo_w para la gráfica
                lista_campo_a.append(campo_a if campo_a != "Sin dato" else 0)
                lista_campo_l.append(campo_l if campo_l != "Sin dato" else 0)
                lista_campo_w.append(campo_w if campo_w != "Sin dato" else 0)

                # Obtener huellas del usuario
                query_huellas = """
                       SELECT mano, tipo_dedo, tipo_huella
                       FROM huellas
                       WHERE iduser = ?
                   """
                cursor.execute(query_huellas, (iduser,))
                huellas = cursor.fetchall()

                # Diccionario para almacenar el tipo de huella en cada dedo
                resultados_dedos = {dedo: "Sin datos" for dedo in nombres_dedos}

                # Rellenar los tipos de huella para cada dedo
                for huella in huellas:
                    mano, tipo_dedo, tipo_huella = huella
                    # Crear clave para verificar con nombres_dedos_map, normalizando a minúsculas
                    dedo_clave = f"{tipo_dedo.capitalize()} {mano.capitalize()}".lower()

                    if dedo_clave in nombres_dedos_map:
                        # Usar el formato estándar de nombres_dedos_map para asignar tipo de huella
                        resultados_dedos[nombres_dedos_map[dedo_clave]] = tipo_huella
                    else:
                        print(f"Advertencia: dedo '{dedo_clave}' no reconocido para usuario {iduser}. "
                              f"Valores - mano: '{mano}', tipo_dedo: '{tipo_dedo}'")

                # Crear la fila de datos para el usuario
                fila = [
                    numero_id, edad, grupo,
                    *[resultados_dedos[dedo] for dedo in nombres_dedos],  # Tipos de huellas en orden
                    sctlmi, sctlmd, sctl_total, campo_a, campo_l, campo_w, d10, diseño
                ]
                datos_exportacion.append(fila)

            # Crear el DataFrame con los datos para exportar a Excel
            columnas = ["Número ID", "Edad","Grupo"] + nombres_dedos + ["SCTL Izquierda", "SCTL Derecha", "SCTL Total",
                                                                "Campo A", "Campo L", "Campo W", "D10", "Diseño"]
            df = pd.DataFrame(datos_exportacion, columns=columnas)

            # Exportar el DataFrame a un archivo Excel
            df.to_excel(archivo, index=False)

            # Crear la gráfica de pastel para las variables campo_a, campo_l y campo_w
            plt.figure(figsize=(10, 6))

            # Graficar Campo A
            plt.subplot(131)  # 1 fila, 3 columnas, gráfico 1
            plt.pie([lista_campo_a.count(i) for i in set(lista_campo_a)], labels=set(lista_campo_a), autopct='%1.1f%%',
                    startangle=90)
            plt.title("Distribución de Campo A")

            # Graficar Campo L
            plt.subplot(132)  # 1 fila, 3 columnas, gráfico 2
            plt.pie([lista_campo_l.count(i) for i in set(lista_campo_l)], labels=set(lista_campo_l), autopct='%1.1f%%',
                    startangle=90)
            plt.title("Distribución de Campo L")

            # Graficar Campo W
            plt.subplot(133)  # 1 fila, 3 columnas, gráfico 3
            plt.pie([lista_campo_w.count(i) for i in set(lista_campo_w)], labels=set(lista_campo_w), autopct='%1.1f%%',
                    startangle=90)
            plt.title("Distribución de Campo W")

            # Guardar la gráfica como una imagen PNG
            grafica_path = 'grafica.png'
            plt.tight_layout()
            plt.savefig(grafica_path)

            # Abrir el archivo Excel con openpyxl
            wb = openpyxl.load_workbook(archivo)
            ws = wb.active

            # Insertar la imagen en la hoja de Excel
            img = Image(grafica_path)
            ws.add_image(img, 'L2')  # Colocar la imagen en la celda L2

            # Guardar el archivo Excel con la imagen añadida
            wb.save(archivo)

            # Mostrar mensaje de éxito
            messagebox.showinfo("Exportación completada",
                                "El archivo se descargó correctamente en Excel.")

            cursor.close()
            return True


        except Exception as e:

            print(f"Ocurrió un error: {e}")  # Mensaje de error en consola

            messagebox.showerror("Error", f"Ocurrió un error: {e}")

            return False




