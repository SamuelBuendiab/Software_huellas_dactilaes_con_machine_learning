import tkinter as tk
from tkinter import ttk

class MainView:
    def __init__(self, root):
        self.root = root
        self.controller = None
        self.root.title("Bienvenido a Análisis de Huellas Dactilares")
        self.root.state('zoomed')

        # Canvas de fondo
        self.canvas = tk.Canvas(self.root, bg='#87CEEB')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Título y subtítulo
        self.titulo = self.canvas.create_text(0, 0, text="Bienvenidos",
                                              font=("Helvetica", 50), fill="black")
        self.subtitulo = self.canvas.create_text(0, 0,
                                                 text="análisis de huellas dactilares",
                                                 font=("Helvetica", 30), fill="black")

        # Crear el estilo para los botones
        estilo_boton = ttk.Style()
        estilo_boton.configure("TButton", font=("Helvetica", 12), background='white', foreground='black', padding=10)

        # Botones de navegación
        self.boton_login = ttk.Button(self.root, text="Iniciar Sesión", style="TButton")
        self.boton_registro = ttk.Button(self.root, text="Registrarse", style="TButton")

        # Colocación de botones en el canvas
        self.login_window = self.canvas.create_window(0, 0, anchor='center', window=self.boton_login)
        self.registro_window = self.canvas.create_window(0, 0, anchor='center', window=self.boton_registro)

        # Vincular el cambio de tamaño de la ventana
        self.root.bind('<Configure>', self.ajustar_ventana)

    def set_controller(self, controller):
        self.controller = controller
        # Reasignar los comandos de los botones después de que se configure el controlador
        self.boton_login.config(command=self.controller.ir_a_login)
        self.boton_registro.config(command=self.controller.ir_a_registro)

    def ajustar_ventana(self, event):
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Ajustar tamaño y posiciones en el canvas
        self.canvas.config(width=width, height=height)
        self.canvas.coords(self.titulo, width // 2, height // 3)
        self.canvas.coords(self.subtitulo, width // 2, height // 2)
        self.canvas.coords(self.login_window, width // 3, height * 5 // 6)
        self.canvas.coords(self.registro_window, width * 2 // 3, height * 5 // 6)


    def mostrar(self):
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Asegúrate de que la vista se muestre correctamente

    def ocultar(self):
        self.canvas.pack_forget()

    def cerrar(self):
        self.root.destroy()


