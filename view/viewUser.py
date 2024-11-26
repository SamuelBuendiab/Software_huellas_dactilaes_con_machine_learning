import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from model.modelUser import ModeloUsuario
from controller.listController import Controlador
from view.fingerprintView import VistaHuellas
import re

class VistaUsuario:
    def __init__(self, root,controlador, parent_window=None):
        self.root = root
        self.controlador = controlador
        self.parent_window = parent_window
        self.root.title("Agregar Usuario")
        self.root.state("zoomed")  # Tamaño de la ventana ajustado
        self.root.configure(bg="#e6f7ff")  # Fondo azul cielo

        # Frame superior con el título
        header_frame = tk.Frame(self.root, bg="#5bbce4")  # Fondo azul más oscuro
        header_frame.pack(fill=tk.X)

        # Título dentro del header
        titulo = tk.Label(header_frame, text="Agregar Usuario", font=("Verdana Bold", 20), fg="white", bg="#5bbce4")
        titulo.pack(side=tk.LEFT, padx=20, pady=10)

        # Colores para el botón
        color_normal = "#33a4d2"  # Color normal del botón
        color_hover = "#e3f2f9"  # Color cuando se pasa el mouse
        color_click = "#0077aa"  # Color cuando se hace clic

        # Botón para volver a la lista de usuarios
        self.boton_cerrar = tk.Button(header_frame, text="Ver lista", command=self.volver_a_lista, bg=color_normal,
                                      fg="white", borderwidth=0, height=2, width=10)
        self.boton_cerrar.pack(side=tk.LEFT, padx=10, pady=10)  # Alineado a la izquierda

        # Cambiar color al pasar el mouse
        self.boton_cerrar.bind("<Enter>", lambda e: self.boton_cerrar.config(bg=color_hover, fg="black"))
        self.boton_cerrar.bind("<Leave>", lambda e: self.boton_cerrar.config(bg=color_normal, fg="white"))

        # Cambiar color al hacer clic
        self.boton_cerrar.bind("<ButtonPress>", lambda e: self.boton_cerrar.config(bg=color_click, fg="white"))
        self.boton_cerrar.bind("<ButtonRelease>", lambda e: self.boton_cerrar.config(bg=color_hover, fg="white"))

        # Frame principal
        main_frame = tk.Frame(self.root, bg="#e6f7ff")
        main_frame.pack(expand=True, fill=tk.BOTH)  # Expandir y llenar el espacio

        # Frame para el formulario y el botón
        form_frame = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RAISED)  # Recuadro para el formulario
        form_frame.pack(pady=20, padx=20, expand=False)  # No expande, solo ocupa el espacio necesario
        form_frame.config(width=650, height=450)  # Ajusta el tamaño del recuadro
        form_frame.place(relx=0.5, rely=0.5, anchor='center')  # Centra el recuadro

        # Título dentro del recuadro
        titulo_formulario = tk.Label(form_frame, text="Agregar Usuario", font=("Verdana Bold", 16), bg="white")
        titulo_formulario.grid(row=0, column=0, pady=10)

        # Crear formulario
        self.crear_formulario(form_frame)

    def crear_formulario(self, frame):
        # Estilo base para las etiquetas e inputs
        styles = {
            'bg': 'white',
            'font': ('Verdana', 12)
        }

        # Crear cada label y entrada en dos columnas
        tk.Label(frame, text="Nombre:", **styles).grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.entry_nombre = tk.Entry(frame, width=30, bd=1, relief=tk.SOLID, font=("Verdana", 12))
        self.entry_nombre.grid(row=2, column=0, padx=20, pady=5)

        tk.Label(frame, text="Grupo:", **styles).grid(row=1, column=1, padx=20, pady=10, sticky='w')
        self.entry_grupo = tk.Entry(frame, width=30, bd=1, relief=tk.SOLID, font=("Verdana", 12))
        self.entry_grupo.grid(row=2, column=1, padx=20, pady=5)

        tk.Label(frame, text="Correo:", **styles).grid(row=3, column=0, padx=20, pady=10, sticky='w')
        self.entry_correo = tk.Entry(frame, width=30, bd=1, relief=tk.SOLID, font=("Verdana", 12))
        self.entry_correo.grid(row=4, column=0, padx=20, pady=5)

        tk.Label(frame, text="Número de ID:", **styles).grid(row=3, column=1, padx=20, pady=10, sticky='w')
        self.entry_numero_id = tk.Entry(frame, width=30, bd=1, relief=tk.SOLID, font=("Verdana", 12))
        self.entry_numero_id.grid(row=4, column=1, padx=20, pady=5)

        tk.Label(frame, text="Número de Celular:", **styles).grid(row=5, column=0, padx=20, pady=10, sticky='w')
        self.entry_numero_celular = tk.Entry(frame, width=30, bd=1, relief=tk.SOLID, font=("Verdana", 12))
        self.entry_numero_celular.grid(row=6, column=0, padx=20, pady=5)

        tk.Label(frame, text="Edad:", **styles).grid(row=5, column=1, padx=20, pady=10, sticky='w')
        self.entry_edad = tk.Entry(frame, width=30, bd=1, relief=tk.SOLID, font=("Verdana", 12))
        self.entry_edad.grid(row=6, column=1, padx=20, pady=5)

        tk.Label(frame, text="Género:", **styles).grid(row=7, column=0, padx=20, pady=10, sticky='w')
        self.entry_genero = ttk.Combobox(frame, width=28, values=["Masculino", "Femenino"], state="readonly",
                                         font=("Verdana", 12))
        self.entry_genero.grid(row=8, column=0, padx=20, pady=5)

        # Botón para agregar usuario
        self.boton_agregar = tk.Button(frame, text="Agregar Usuario", command=self.agregar_usuario, bg="#5bbce4",
                                       fg="white", borderwidth=0, height=2, width=15)
        self.boton_agregar.grid(row=9, columnspan=2, pady=20)
        self.boton_agregar.bind("<Enter>", lambda e: self.boton_agregar.config(bg="#66c2ff"))
        self.boton_agregar.bind("<Leave>", lambda e: self.boton_agregar.config(bg="#5bbce4"))

    def agregar_usuario(self):
        nombre = self.entry_nombre.get()
        grupo = self.entry_grupo.get()
        correo = self.entry_correo.get()
        numero_id = self.entry_numero_id.get()
        numero_celular = self.entry_numero_celular.get()
        edad = self.entry_edad.get()
        genero = self.entry_genero.get()

        # Verificaciones de los campos
        if not nombre or not grupo or not correo or not numero_id or not numero_celular or not edad or not genero:
            messagebox.showwarning("Advertencia", "Por favor completa todos los campos")
            return

        if not self.validar_nombre(nombre):
            messagebox.showerror("Error", "El nombre debe contener solo letras.")
            return

        if not self.validar_grupo(grupo):
            messagebox.showerror("Error", "El Grupo debe contener solo letras.")
            return

        if not self.validar_correo(correo):
            messagebox.showerror("Error", "El correo electrónico no es válido.")
            return

        if not self.validar_numero(numero_id):
            messagebox.showerror("Error", "El número ID debe ser un valor numérico.")
            return

        if not self.validar_numero(numero_celular):
            messagebox.showerror("Error", "El número celular debe ser un valor numérico.")
            return

        if not self.validar_numero(edad):
            messagebox.showerror("Error", "La edad debe ser un valor numérico.")
            return


        if nombre and grupo and correo and numero_id and numero_celular and edad and genero:
            modelo = ModeloUsuario()
            user_id = modelo.agregar_usuario(nombre, grupo, correo, numero_id, numero_celular, edad, genero)
            if user_id:
                messagebox.showinfo("Éxito", "Usuario agregado correctamente")
                self.entry_nombre.delete(0, tk.END)
                self.entry_grupo.delete(0, tk.END)
                self.entry_correo.delete(0, tk.END)
                self.entry_numero_id.delete(0, tk.END)
                self.entry_numero_celular.delete(0, tk.END)
                self.entry_edad.delete(0, tk.END)
                self.entry_genero.set('')
                self.abrir_vista_huellas(user_id, nombre)
            else:
                messagebox.showerror("Error", "No se pudo agregar el usuario.")

    def validar_nombre(self, nombre):
        return all(c.isalpha() or c.isspace() for c in nombre)

    def validar_grupo(self, grupo):
        return all(c.isalpha() or c.isspace() for c in grupo)

    def validar_correo(self, correo):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(regex, correo) is not None



    def validar_numero(self, numero):
        return numero.isdigit()

    def abrir_vista_huellas(self, user_id, user_name):
        self.root.destroy()
        nuevo_root = tk.Toplevel()
        VistaHuellas(nuevo_root, user_id, user_name)

    def volver_a_lista(self):
        self.root.destroy()
        from view import inicio
        nuevo_root = tk.Tk()  # Crea una nueva ventana
        controlador_inicio = inicio.Controlador()  # Asegúrate de que este controlador esté bien definido
        vista_inicio = inicio.VistaUsuarios(controlador_inicio, nuevo_root)  # Pasa la nueva ventana como argumento
        nuevo_root.mainloop()  # Muestra la ventana principal existente
        self.parent_window.state("zoomed")

    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Quieres cerrar la aplicación?"):
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

# Para ejecutar la ventana de agregar usuario
#if __name__ == "__main__":
#    root = tk.Tk()
#    app = VistaUsuario(root)
#    root.mainloop()