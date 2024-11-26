from model.modelUser import ModeloUsuario

class ControladorUsuario:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = ModeloUsuario()

    def agregar_usuario(self, nombre, grupo, correo, numero_id, numero_celular, edad, genero, idhuellas=None):
        # Llamamos al modelo para agregar el usuario y obtener el user_id
        user_id = self.modelo.agregar_usuario(nombre, grupo, correo, numero_id, numero_celular, edad, genero, idhuellas)


        # Retornamos el user_id para que la vista lo pueda usar
        if user_id:
            return user_id
        else:
            # En caso de error, podemos manejarlo aquí o en la vista
            return None


