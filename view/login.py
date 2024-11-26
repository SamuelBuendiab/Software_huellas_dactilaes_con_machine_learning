import tkinter as tk

from tkinter import ttk
from model.dbConnetion import conectar
from view.inicio import VistaUsuarios
from controller.listController import Controlador
from controller.controller import Controller

class LoginView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Formulario de Login")
        self.root.state('zoomed')  # Para que ocupe toda la pantalla
        self.root.configure(bg='#87CEEB')

        canvas = tk.Canvas(self.root, bg='#87CEEB', width=self.root.winfo_screenwidth(),
                           height=self.root.winfo_screenheight())
        canvas.pack(fill="both", expand=True)

        # Botón Atrás
        estilo_boton = ttk.Style()
        estilo_boton.configure("TButton", font=("Helvetica", 12), background='white', foreground='black', padding=10)
        boton_atras = ttk.Button(self.root, text="← Atrás", style="TButton", command=self.volver_al_main)
        canvas.create_window(50, 50, anchor='nw', window=boton_atras)

        frame = tk.Frame(canvas, bg='white', padx=50, pady=50)
        canvas.create_window(self.root.winfo_screenwidth() // 2, self.root.winfo_screenheight() // 2, window=frame)

        # Correo electrónico
        tk.Label(frame, text="Correo:", bg='white', font=("Helvetica", 14)).grid(row=0, column=0, pady=10, padx=5)
        self.entry_correo = tk.Entry(frame, font=("Helvetica", 14))
        self.entry_correo.grid(row=0, column=1, pady=10, padx=5)

        # Contraseña
        tk.Label(frame, text="Contraseña:", bg='white', font=("Helvetica", 14)).grid(row=1, column=0, pady=10, padx=5)
        self.entry_contraseña = tk.Entry(frame, show="*", font=("Helvetica", 14))
        self.entry_contraseña.grid(row=1, column=1, pady=10, padx=5)

        # Botón para iniciar sesión
        boton_login = ttk.Button(frame, text="Iniciar Sesión", style="TButton", command=self.verificar_login)
        boton_login.grid(row=2, columnspan=2, pady=20)

    def volver_al_main(self):
        self.root.withdraw()  # Ocultamos la ventana de login
        self.controller.ir_a_main()  # Llama al método del controlador para volver a la vista principal

    def verificar_login(self):
        correo = self.entry_correo.get()
        contraseña = self.entry_contraseña.get()

        if self.controller.iniciar_sesion(correo, contraseña):
            self.cerrar_ventana()  # Cierra la ventana de login si el inicio de sesión es exitoso

        else:

            pass


    def cerrar_ventana(self):
        # Solo decrementa el contador y cierra si es necesario
        self.controller.cerrar_ventana()  # Decrementar el contador
        self.root.destroy()  # Cerrar la ventana de login



def abrir_ventana_login(controller):
    ventana_login = tk.Toplevel()  # Crear una ventana secundaria para el login
    ventana_login.transient(controller.root)  # Hacer la ventana dependiente de la principal
    login_view = LoginView(ventana_login, controller)  # Crear la vista de login
    ventana_login.mainloop()

def ocultar(self):
    self.root.withdraw()






