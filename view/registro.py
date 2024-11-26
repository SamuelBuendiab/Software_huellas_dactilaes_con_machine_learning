import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from model.dbConnetion import conectar
import sqlite3


class RegistroView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_ventana)
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Formulario de Registro")
        self.root.state('zoomed')  # Para que ocupe toda la pantalla
        self.root.configure(bg='#87CEEB')  # Fondo azul claro

        canvas = tk.Canvas(self.root, bg='#87CEEB', width=self.root.winfo_screenwidth(),
                           height=self.root.winfo_screenheight())
        canvas.pack(fill="both", expand=True)

        # Botón Atrás
        estilo_boton = ttk.Style()
        estilo_boton.configure("TButton", font=("Helvetica", 12), background='white', foreground='black', padding=10)
        boton_atras = ttk.Button(self.root, text="← Atrás", style="TButton",
                                 command=self.volver_al_main)
        canvas.create_window(50, 50, anchor='nw', window=boton_atras)

        frame = tk.Frame(canvas, bg='white', padx=50, pady=50)
        canvas.create_window(self.root.winfo_screenwidth() // 2, self.root.winfo_screenheight() // 2, window=frame)

        # Nombre de usuario
        tk.Label(frame, text="Nombre de Usuario:", bg='white', font=("Helvetica", 14)).grid(row=0, column=0, pady=10, padx=5)
        self.entry_nombre_usuario = tk.Entry(frame, font=("Helvetica", 14))
        self.entry_nombre_usuario.grid(row=0, column=1, pady=10, padx=5)

        # Correo electrónico
        tk.Label(frame, text="Correo:", bg='white', font=("Helvetica", 14)).grid(row=1, column=0, pady=10, padx=5)
        self.entry_correo = tk.Entry(frame, font=("Helvetica", 14))
        self.entry_correo.grid(row=1, column=1, pady=10, padx=5)

        # Contraseña
        tk.Label(frame, text="Contraseña:", bg='white', font=("Helvetica", 14)).grid(row=2, column=0, pady=10, padx=5)
        self.entry_contraseña = tk.Entry(frame, show="*", font=("Helvetica", 14))
        self.entry_contraseña.grid(row=2, column=1, pady=10, padx=5)

        # Botón para registrar
        boton_registrar = ttk.Button(frame, text="Registrar", style="TButton", command=self.registrar_usuario)
        boton_registrar.grid(row=3, columnspan=2, pady=20)

    def volver_al_main(self):
        self.root.withdraw()
        self.controller.ir_a_main()  # Llama a la función para abrir la ventana de login

    def registrar_usuario(self):
        conexion = conectar()
        if conexion is None:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
            return

        cursor = conexion.cursor()

        nombre_usuario = self.entry_nombre_usuario.get()
        correo = self.entry_correo.get()
        contraseña = self.entry_contraseña.get()

        try:
            cursor.execute('SELECT * FROM registro WHERE correo = ?', (correo,))
            if cursor.fetchone():
                messagebox.showerror("Error", "El correo ya está registrado.")
            else:
                cursor.execute('''
                    INSERT INTO registro (nombre_usuario, correo, contraseña)
                    VALUES (?, ?, ?)
                ''', (nombre_usuario, correo, contraseña))

                conexion.commit()
                messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
                self.root.withdraw()
                self.controller.ir_a_main()


        except sqlite3.Error as err:
            messagebox.showerror("Error", f"Error al registrar el usuario: {err}")

        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def cerrar_ventana(self):
        self.controller.cerrar_ventana()  # Decrementar el contador y cerrar si es necesario
        self.root.destroy()  # Cerrar la ventana de

def abrir_ventana_registro(controller):
    ventana_registro = tk.Toplevel()  # Usar Toplevel en lugar de Tk
    ventana_registro.transient(controller.root)  # Hacer la ventana dependiente de la principal
    registro_view = RegistroView(ventana_registro, controller)




