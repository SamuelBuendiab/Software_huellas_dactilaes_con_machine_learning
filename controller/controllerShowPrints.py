
from model.modelShowPrints import ModeloHuellas

class ControladorHuellas:
    def __init__(self):
        self.modelo_huellas = ModeloHuellas()

    def obtener_huellas_usuario(self, user_id):
        huellas = self.modelo_huellas.obtener_huellas_usuario(user_id)
        print(f"Huellas recibidas en el controlador: {huellas}")
        return huellas

    def obtener_calculo_usuario(self, user_id):
        calculo = self.modelo_huellas.obtener_calculos_usuario(user_id)
        print(f"datos recibidos en el controlador: {calculo}")
        return calculo