import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from controller.controllerShowPrints import ControladorHuellas
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

class VistaHuellasUsuario:
    def __init__(self, root, user_id, nombre_paciente, vista_usuarios):
        self.root = root
        self.user_id = user_id
        self.nombre_paciente = nombre_paciente  # Agregar el nombre del paciente
        self.controlador = ControladorHuellas()
        self.vista_usuarios = vista_usuarios  # Guardar referencia a la vista de usuarios
        self.dedos = ["Pulgar Derecho", "Índice Derecho", "Medio Derecho", "Anular Derecho", "Meñique Derecho",
                      "Pulgar Izquierdo", "Índice Izquierdo", "Medio Izquierdo", "Anular Izquierdo",
                      "Meñique Izquierdo"]
        self.imagenes = []
        # Obtener las huellas desde el controlador usando el user_id
        self.huellas = self.controlador.obtener_huellas_usuario(self.user_id)
        self.calculos = self.controlador.obtener_calculo_usuario(self.user_id)  # Obtener cálculos
        print(f"Huellas en la vista: {self.huellas}")  # Imprimir para verificar los datos
        print(f"Cálculos en la vista: {self.calculos}")  # Imprimir para verificar los cálculos

        self.root.title(f"Huellas de Usuario {self.nombre_paciente}")
        self.root.geometry("1200x800")
        self.root.config(bg='#f0f8ff')  # Fondo azul claro

        # Crear la interfaz de usuario
        self.crear_ui()

    def crear_ui(self):

        # Contenedor de botones centrados en la parte inferior
        self.frame_botones = tk.Frame(self.root, bg='#f0f8ff')
        self.frame_botones.grid(row=0, column=0, columnspan=2, pady=(10, 10))

        # Botón para volver a la lista
        self.boton_volver = tk.Button(self.frame_botones, text="Volver a Lista", command=self.volver_a_lista,
                                      bg='#87CEEB', fg='white', borderwidth=0, height=2, width=15)
        self.boton_volver.grid(row=0, column=0, padx=10)  # Cambiado a grid

        # Cambiar color al pasar el mouse
        self.boton_volver.bind("<Enter>", lambda e: self.boton_volver.config(bg='#4682B4', fg='black'))
        self.boton_volver.bind("<Leave>", lambda e: self.boton_volver.config(bg='#87CEEB', fg='white'))

        # Cambiar color al hacer clic
        self.boton_volver.bind("<ButtonPress>", lambda e: self.boton_volver.config(bg='#1E90FF', fg='white'))
        self.boton_volver.bind("<ButtonRelease>", lambda e: self.boton_volver.config(bg='#87CEEB', fg='white'))

        # Botón para descargar en PDF
        self.boton_pdf = tk.Button(self.frame_botones, text="Descargar en PDF", command=self.descargar_pdf,
                                   bg='#4682B4', fg='white', borderwidth=0, height=2, width=20)
        self.boton_pdf.grid(row=0, column=1, padx=10)  # Cambiado a grid

        # Cambiar color al pasar el mouse
        self.boton_pdf.bind("<Enter>", lambda e: self.boton_pdf.config(bg='#87CEEB', fg='black'))
        self.boton_pdf.bind("<Leave>", lambda e: self.boton_pdf.config(bg='#4682B4', fg='white'))

        # Cambiar color al hacer clic
        self.boton_pdf.bind("<ButtonPress>", lambda e: self.boton_pdf.config(bg='#1E90FF', fg='white'))
        self.boton_pdf.bind("<ButtonRelease>", lambda e: self.boton_pdf.config(bg='#87CEEB', fg='white'))

        # Label para mostrar el nombre del paciente
        label_paciente = tk.Label(self.root, text=f"Paciente: {self.nombre_paciente}", bg='#f0f8ff', font=('Arial', 12))
        label_paciente.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky='w')  # Colocar en la parte superior central


        # Contenedor de tarjetas de huellas
        self.frame_tarjetas = tk.Frame(self.root, bg='#f0f8ff')
        self.frame_tarjetas.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Hacer que el frame_tarjetas sea responsivo
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Crear tarjetas con los datos de las huellas
        self.crear_tarjetas()

        # Contenedor para cálculos
        self.frame_calculos = tk.Frame(self.root, bg='#f0f8ff')
        self.frame_calculos.grid(row=2, column=0, columnspan=2, pady=(10, 10), padx=10)

        # Mostrar resultados de cálculos
        self.mostrar_calculos()

    def mostrar_calculos(self):
        style = ttk.Style(self.root)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="white", foreground="black")
        style.configure("Treeview", rowheight=25, font=("Arial", 12))  # Reducir el tamaño de la fuente

        num_columns = len(self.calculos)
        self.tabla = ttk.Treeview(self.frame_calculos, columns=list(self.calculos.keys()), show="headings",
                                  height=1)  # Altura de una fila
        self.tabla.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")  # Mover la tabla a la columna 1

        for key in self.calculos.keys():
            self.tabla.heading(key, text=key)
            self.tabla.column(key, width=80, anchor="center")  # Reducir el ancho de las columnas

        self.tabla.tag_configure("oddrow", background="#e6f7ff")
        self.tabla.tag_configure("evenrow", background="#ccf2ff")

        valores = tuple(dict(self.calculos).values())
        self.tabla.insert("", "end", values=valores, tags=("evenrow",))

        # Crear y colocar la etiqueta a la izquierda de la tabla
        label_calculos = tk.Label(self.frame_calculos, text="Resultados de Cálculos:", bg='#f0f8ff',
                                  font=('Arial', 10, 'bold'))
        label_calculos.grid(row=1, column=0, padx=10, pady=10, sticky="w")  # Colocar la etiqueta en la columna 0

        # Ajustar el comportamiento de las columnas y filas
        self.frame_calculos.grid_columnconfigure(0, weight=0)  # Columna de la etiqueta
        self.frame_calculos.grid_columnconfigure(1, weight=1)  # Columna de la tabla
        self.frame_calculos.grid_rowconfigure(1, weight=1)  # Fila de la tabla y la etiqueta

    def refrescar_huellas(self):
        # Limpiar el contenido del frame de tarjetas
        for widget in self.frame_tarjetas.winfo_children():
            widget.destroy()  # Eliminar cada widget existente en el contenedor

            # Obtener las huellas y cálculos nuevamente desde el controlador
            self.huellas = self.controlador.obtener_huellas_usuario(self.user_id)
            self.calculos = self.controlador.obtener_calculo_usuario(self.user_id)  # Obtener cálculos
            print(f"Refrescando huellas para el usuario {self.user_id}. Nuevas huellas: {self.huellas}")
            print(f"Nuevos cálculos: {self.calculos}")

        # Volver a crear las tarjetas con las nuevas huellas
        self.crear_tarjetas()

    def crear_tarjetas(self):
        self.huellas = self.controlador.obtener_huellas_usuario(self.user_id)

        for widget in self.frame_tarjetas.winfo_children():
            widget.destroy()

        if not self.huellas:
            tk.Label(self.frame_tarjetas, text="No se encontraron huellas.", bg='#f0f8ff').pack()
            return

        for index, huella in enumerate(self.huellas):
            if index >= 10:
                break

            tipo_dedo_completo = f"{huella['tipo_dedo']} {huella['mano']}"
            tipo_huella = huella['tipo_huella']

            frame_tarjeta = tk.Frame(self.frame_tarjetas, bd=2, relief=tk.RAISED, padx=5, pady=5, bg='#ffffff',
                                     width=120, height=120)  # Reducir el tamaño de las tarjetas
            frame_tarjeta.grid_propagate(False)
            frame_tarjeta.grid(row=index // 5, column=index % 5, padx=5, pady=5, sticky="nsew")

            self.frame_tarjetas.grid_rowconfigure(index // 5, weight=1)
            self.frame_tarjetas.grid_columnconfigure(index % 5, weight=1)

            tk.Label(frame_tarjeta, text=tipo_dedo_completo, bg='#ffffff', font=('Arial', 10, 'bold')). pack(pady=(5, 0))

            tk.Label(frame_tarjeta, text=f"Tipo de Huella: {tipo_huella}", bg='#ffffff',
                     font=('Arial', 10)).pack(pady=(5, 0))

            resultado_analisis = huella['resultado_analisis']
            if tipo_huella.lower() in ["presilla", "verticilo"]:
                tk.Label(frame_tarjeta, text=f"Resultado Análisis: {resultado_analisis}", bg='#ffffff',
                         font=('Arial', 9)).pack(pady=(5, 10))
            elif tipo_huella.lower() != "arco":
                tk.Label(frame_tarjeta, text=f"Análisis: {resultado_analisis}", bg='#ffffff',
                         font=('Arial', 10, 'italic')).pack(pady=(5, 0))

            imagen_path = huella['imagen_path']
            if os.path.exists(imagen_path):
                try:
                    img = Image.open(imagen_path)
                    img = img.resize((120, 120))  # Ajustar tamaño de la imagen
                    img_tk = ImageTk.PhotoImage(img)

                    label_imagen = tk.Label(frame_tarjeta, image=img_tk, bg='#ffffff')
                    label_imagen.image = img_tk
                    label_imagen.pack(padx=5, pady=5)
                except Exception as e:
                    print(f"Error al cargar la imagen: {e}")


    def descargar_pdf(self):
        """Genera y guarda un PDF con las huellas del usuario."""
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not pdf_path:
            return  # Si no se seleccionó ninguna ruta, salir de la función

        try:
            c = canvas.Canvas(pdf_path, pagesize=letter)
            c.setFont("Helvetica", 12)

            # Agregar título
            c.drawString(100, 750, "Análisis de Huellas")

            # Agregar subtítulo con el ID del usuario
            c.setFont("Helvetica", 10)
            c.drawString(100, 735, f"Huellas de Usuario: {self.nombre_paciente}")


            # Restablecer el tamaño de la fuente para el contenido
            c.setFont("Helvetica", 12)

            # Agregar información de las huellas
            y_position = 700
            for index, huella in enumerate(self.huellas):
                # Agregar nombre del dedo
                tipo_dedo = self.dedos[index] if index < len(self.dedos) else "Dedo Desconocido"
                c.drawString(100, y_position, f"Dedo: {tipo_dedo}")

                # Agregar imagen
                imagen_path = huella['imagen_path']
                img = ImageReader(imagen_path)
                c.drawImage(img, 100, y_position - 50, width=50, height=50,
                            preserveAspectRatio=True)  # Agregar la imagen

                # Agregar tipo de huella
                c.drawString(160, y_position - 20, f"Tipo de Huella: {huella['tipo_huella']}")

                # Agregar resultado de análisis si no es "arco"
                if huella['tipo_huella'].lower() != "arco":
                    c.drawString(160, y_position - 40, f"Resultado Análisis: {huella['resultado_analisis']}")

                c.drawString(160, y_position - 60, "-------------------------------------")
                y_position -= 80  # Espaciado entre huellas

                if y_position < 50:  # Si llega al final de la página, crear una nueva
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y_position = 750

            c.save()
            messagebox.showinfo("Éxito", "PDF descargado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")

    def volver_a_lista(self):
        self.root.destroy()  # Cerrar la ventana actual
        if self.vista_usuarios:
            self.vista_usuarios.deiconify()  # Mostrar la ventana de gestión de usuarios nuevamente
            self.vista_usuarios.state("zoomed")
    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Quieres cerrar la aplicación?"):
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
