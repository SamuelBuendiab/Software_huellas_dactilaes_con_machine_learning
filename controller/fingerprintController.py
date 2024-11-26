from model.modelFingerprint import ModeloHuellas
from tkinter import filedialog, messagebox

class ControladorHuellas:
    def __init__(self):
        self.modelo_huellas = ModeloHuellas()

    def seleccionar_imagen(self):
        # Usamos filedialog.askopenfilename para seleccionar archivos de imagen
        imagen_path = filedialog.askopenfilename(
            title="Selecciona una imagen de huella",
            filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")],  # Filtros de archivos
            initialdir=r"C:\Users\%USERNAME%\Desktop"  # Inicializar el diálogo en el escritorio
        )
        return imagen_path
    def guardar_imagen(self, user_id, user_name, imagen_path, dedo):
        # Guardar la imagen en la carpeta del usuario
        if imagen_path:
            return self.modelo_huellas.guardar_imagen(user_id, user_name, imagen_path, dedo)
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ninguna imagen")

    def guardar_datos_huella(self, user_id, tipo_huella, resultado_analisis, imagen_path, mano, tipo_dedo):
        # Guardar los datos de la huella en la base de datos junto con la ruta de la imagen
        if tipo_huella and resultado_analisis and imagen_path:
            if self.modelo_huellas.guardar_huella_en_bd(user_id, tipo_huella, resultado_analisis, imagen_path, mano, tipo_dedo):
                return True
            else:
                return False
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos antes de guardar.")
            return False

    def obtener_huellas_usuario(self, user_id):
        return self.modelo_huellas.obtener_huellas_usuario(user_id)


    def caluarcular(self, user_id, comentario):
        return self.modelo_huellas.calcular_campos(user_id, comentario)

