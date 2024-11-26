import subprocess
from model.modelUser import ModeloUsuario
from model.modelFingerprint import ModeloHuellas
from tkinter import messagebox, filedialog

class Controlador:
    def __init__(self):
        self.modelo = ModeloUsuario()
        self.modeloH=ModeloHuellas()

    def obtener_usuarios(self):
        return self.modelo.obtener_usuarios()

    def eliminar_usuario(self, user_id):
        self.modelo.eliminar_usuario(user_id)


    def actualizar_usuario(self, user_id, grupo, nombre, correo, numero_id, numero_celular, edad, genero):
        return self.modelo.actualizar_usuario(user_id, nombre, grupo, correo, numero_id, numero_celular, edad, genero)

    def importar_sql(self, archivo_sql):
        try:
            comando = f"mysql -u root -p < {archivo_sql}"
            subprocess.run(comando, shell=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error al importar SQL: {e}")
            return False

    def exportar_a_excel(self, archivo,grupo):
        self.modeloH.exportar_a_excel(archivo,grupo)

    def reporte_guardar(self, fecha_hora_inicio, fecha_hora_fin,archivo_destino):
        # Llama al método generar_reporte en el modelo
        self.modelo.generar_reporte(fecha_hora_inicio, fecha_hora_fin, archivo_destino)


    def iniciar(self):
        from view.inicio import VistaUsuarios
        self.vista = VistaUsuarios(self)
        self.vista.mainloop()

#if __name__ == "__main__":
#    controlador = Controlador()
#    controlador.iniciar()
