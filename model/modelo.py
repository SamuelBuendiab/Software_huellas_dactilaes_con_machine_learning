class Modelo:
    def __init__(self):
        self.datos = {}

    def obtener_datos(self):
        return self.datos

    def guardar_usuario(self, username, password):
        self.datos[username] = password

    def verificar_usuario(self, username, password):
        return username in self.datos and self.datos[username] == password