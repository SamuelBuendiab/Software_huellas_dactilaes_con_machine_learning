import sqlite3
from tkinter import messagebox
from model.dbConnetion import conectar
from view.inicio import VistaUsuarios
from controller.listController import Controlador


class Controller:
    def __init__(self, root, modelo, vista_principal, controller_principal=None):
        self.controller_principal = controller_principal
        self.modelo = modelo
        self.root = root
        self.vista_principal = vista_principal  # MainView debería asignarse aquí
        self.vista_actual = self.vista_principal  # La vista inicial es la vista principal
        self.window_count = 0

    def gestionar_evento(self):
        datos = self.modelo.obtener_datos()
        self.vista_actual.actualizar_vista(datos)  # Usa vista_actual en lugar de vista

    def ir_a_login(self):
        from view.login import abrir_ventana_login
        if self.vista_actual is not None:
            self.vista_actual.ocultar()  # Ocultamos la vista actual
        self.vista_actual = None  # Limpiamos la referencia a la vista actual
        self.window_count += 1  # Incrementar el contador de ventanas abiertas
        abrir_ventana_login(self)  # Abrimos la ventana de login

    def ir_a_registro(self):
        from view.registro import abrir_ventana_registro
        if self.vista_actual is not None:
            self.vista_actual.ocultar()  # Ocultamos la vista actual
        self.vista_actual = None  # Limpiamos la referencia a la vista actual
        self.window_count += 1  # Incrementar el contador de ventanas abiertas
        abrir_ventana_registro(self)  # Abrimos la ventana de registro

    def ir_a_main(self):
        if self.vista_actual and self.vista_actual != self.vista_principal:
            self.vista_actual.ocultar()  # Ocultamos la vista actual si no es la principal
        self.vista_principal.mostrar()  # Mostramos la ventana principal
        self.vista_actual = self.vista_principal  # Actualizamos la vista actual

    def cerrar_ventana(self):
        self.window_count -= 1  # Decrementar el contador de ventanas abiertas
        if self.window_count == 0:
            self.cerrar_ventana_principal()  # Cerrar la ventana principal si no hay ventanas abiertas

    def iniciar_sesion(self, correo, contraseña):
        # Conectar a la base de datos
        conexion = conectar()
        if conexion:
            cursor = conexion.cursor()

            # Primero, verificamos si el correo existe
            cursor.execute('''SELECT * FROM registro WHERE correo = ?''', (correo,))
            usuario = cursor.fetchone()

            if usuario:
                # Si el correo existe, verificamos la contraseña
                cursor.execute('''SELECT * FROM registro WHERE correo = ? AND contraseña = ?''', (correo, contraseña))
                result = cursor.fetchone()

                if result:
                    messagebox.showinfo("Éxito", "Ingreso exitoso!")
                    self.root.destroy()

                    # Inicializar directamente la vista de usuarios
                    controlador = Controlador()
                    app = VistaUsuarios(controlador)

                    # Mostrar la ventana principal
                    app.root.mainloop()
                    return True

                else:
                    # La contraseña es incorrecta
                    messagebox.showerror("Error", "La contraseña es incorrecta.")
                    return False
            else:
                # El correo no existe
                messagebox.showerror("Error", "El correo no está registrado.")
                return False

            conexion.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return False

    def cerrar_ventana_principal(self):
        self.root.destroy()



