import tkinter as tk
from tkinter import filedialog, messagebox
import os

from Pruebaimagenes.test import predecir_tipo_huella, model, tipo_huella
from Pruebaimagenes.new7 import FingerprintAnalysis
from controller.listController import Controlador
from controller.fingerprintController import ControladorHuellas
from PIL import Image, ImageTk  # Para manejar las imágenes

class VistaHuellas:
    def __init__(self, root, user_id, user_name):
        self.root = root
        self.root.title("Registro de Huellas")
        self.root.state("zoomed")
        self.root.config(bg='#f0f8ff')  # Fondo azul claro
        self.controlador = ControladorHuellas()
        self.user_id = user_id
        self.user_name = user_name
        self.dedos = ["Pulgar Derecho", "Indice Derecho", "Medio Derecho", "Anular Derecho", "Menique Derecho",
                      "Pulgar Izquierdo", "Indice Izquierdo", "Medio Izquierdo", "Anular Izquierdo",
                      "Menique Izquierdo"]

        self.tarjetas = []  # Lista para almacenar referencias a las tarjetas
        self.crear_ui()

    def crear_ui(self):

        # Colores para el botón
        color_normal = "#33a4d2"  # Color normal del botón
        color_hover = "#52afda"  # Color cuando se pasa el mouse
        color_click = "#0077aa"  # Color cuando se hace clic
        # Botón para volver a la lista
        self.boton_volver = tk.Button(self.root, text="Volver a Lista", command=self.volver_a_lista, bg=color_normal,
                                      fg="white", borderwidth=0, height=2, width=15)
        self.boton_volver.pack(anchor="nw", padx=10, pady=10)  # Alineado al noroeste

        # Cambiar color al pasar el mouse
        self.boton_volver.bind("<Enter>", lambda e: self.boton_volver.config(bg=color_hover, fg="black"))
        self.boton_volver.bind("<Leave>", lambda e: self.boton_volver.config(bg=color_normal, fg="white"))

        # Cambiar color al hacer clic
        self.boton_volver.bind("<ButtonPress>", lambda e: self.boton_volver.config(bg=color_click, fg="white"))
        self.boton_volver.bind("<ButtonRelease>", lambda e: self.boton_volver.config(bg=color_hover, fg="white"))

        # Canvas para permitir el scroll
        self.canvas = tk.Canvas(self.root, bg='#f0f8ff')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar para el Canvas
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame dentro del Canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg='#f0f8ff')
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Crear ventana en el canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Contenedor de tarjetas de huellas
        self.frame_tarjetas = tk.Frame(self.scrollable_frame, bg='#f0f8ff')
        self.frame_tarjetas.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Crear tarjetas
        self.crear_tarjetas()

        # Recuadro para comentarios
        self.texto_comentario = tk.Text(self.scrollable_frame, height=5, width=70, bg='#ffffff', font=('Arial', 10))
        self.texto_comentario.insert(tk.END, "Escribe aquí tu diagnóstico")  # Texto por defecto

        def on_click(event):
            if self.texto_comentario.get("1.0", tk.END) == "Escribe aquí tu diagnóstico\n":
                self.texto_comentario.delete("1.0", tk.END)
                self.texto_comentario.config(fg='black')

        def on_focusout(event):
            if self.texto_comentario.get("1.0", tk.END) == "\n":
                self.texto_comentario.insert(tk.END, "Escribe aquí tu diagnóstico")
                self.texto_comentario.config(fg='grey')

        self.texto_comentario.bind("<FocusIn>", on_click)
        self.texto_comentario.bind("<FocusOut>", on_focusout)
        self.texto_comentario.config(fg='grey')  # Texto gris por defecto

        self.texto_comentario.pack(pady=(10, 10), fill=tk.X, padx=20)

        # Botón para guardar los datos
        self.boton_guardar = tk.Button(self.scrollable_frame, text="Guardar Datos", command=self.guardar_datos,
                                       bg="#5bbce4", fg="white", borderwidth=0, height=2, width=15)
        self.boton_guardar.pack(pady=20)

        # Cambiar color al pasar el mouse
        self.boton_guardar.bind("<Enter>", lambda e: self.boton_guardar.config(bg="#66c2ff"))
        self.boton_guardar.bind("<Leave>", lambda e: self.boton_guardar.config(bg="#5bbce4"))

    def crear_tarjetas(self):
        # Crear tarjetas y ajustar la distribución
        for index, dedo in enumerate(self.dedos):
            tarjeta = self.crear_tarjeta(index, dedo)
            self.tarjetas.append(tarjeta)  # Agregar tarjeta a la lista

    def crear_tarjeta(self, index, dedo):
        frame = tk.Frame(self.frame_tarjetas, bd=2, relief=tk.RAISED, padx=10, pady=10, bg='#ffffff')  # Fondo blanco para las tarjetas
        frame.grid(row=index // 5, column=index % 5, padx=10, pady=10, sticky='nsew')

        # Hacer que la tarjeta sea responsiva
        self.frame_tarjetas.grid_rowconfigure(index // 5, weight=1)
        self.frame_tarjetas.grid_columnconfigure(index % 5, weight=1)

        try:
            self.default_img = Image.open("images/default.png").resize((150, 150))  # Imagen por defecto
        except FileNotFoundError:
            self.default_img = Image.new("RGB", (150, 150), "lightgray")  # Fondo gris si no hay imagen
        img = ImageTk.PhotoImage(self.default_img)
        label_imagen = tk.Label(frame, image=img, bg='#ffffff')
        label_imagen.image = img  # Mantener una referencia a la imagen
        label_imagen.pack()

        # Nombre del dedo
        label_dedo = tk.Label(frame, text=dedo, bg='#ffffff', font=('Arial', 10, 'bold'))
        label_dedo.pack(pady=(5, 10))  # Espaciado vertical

        # Label para tipo de huella
        label_tipo_huella = tk.Label(frame, text="Tipo de huella", bg='#ffffff', font=('Arial', 10))
        label_tipo_huella.pack(pady=(10, 5))  # Espaciado vertical

        # Nuevo Label para mostrar el tipo de huella
        label_tipo_huella_value = tk.Label(frame, text={tipo_huella}, bg='#ffffff', font=('Arial', 10, 'italic'))
        label_tipo_huella_value.pack(pady=5)

        # Label para numeración
        label_entero = tk.Label(frame, text="Numeración", bg='#ffffff', font=('Arial', 10))
        label_entero.pack(pady=(10, 5))  # Espaciado vertical

        # Nuevo Label para mostrar el valor
        label_entero_value = tk.Label(frame, text="1", bg='#ffffff', font=('Arial', 10, 'italic'))
        label_entero_value.pack(pady=5)

        # Ocultar temporalmente el tipo de huella y la numeración
        label_tipo_huella.pack_forget()
        label_tipo_huella_value.pack_forget()
        label_entero.pack_forget()
        label_entero_value.pack_forget()

        # Vincular evento de clic a la tarjeta completa
        frame.bind("<Button-1>", lambda event, d=dedo, l=label_imagen: self.cargar_imagen(d, l))
        label_imagen.bind("<Button-1>", lambda event, d=dedo, l=label_imagen: self.cargar_imagen(d, l))

        # Animación de hover para la tarjeta
        frame.bind("<Enter>", lambda e: self.animar_tarjeta(frame, hover=True))
        frame.bind("<Leave>", lambda e: self.animar_tarjeta(frame, hover=False))

        return {
            "frame": frame,
            "label_dedo": label_dedo,
            "label_tipo_huella": label_tipo_huella,
            "label_entero": label_entero,
            "label_imagen": label_imagen,
            "imagen_path": None,  # Almacenar la ruta de la imagen
            "label_tipo_huella_value": label_tipo_huella_value,
            "label_entero_value": label_entero_value
        }

    def animar_tarjeta(self, frame, hover):
        if hover:
            frame.config(bg='#e0f7fa', bd=4)  # Cambia el color de fondo y el borde
        else:
            frame.config(bg='#ffffff', bd=2)  # Restaura el color original y el borde

    def cargar_imagen(self, dedo, label_imagen):
        imagen_path = self.controlador.seleccionar_imagen()
        if imagen_path:
            try:
                # Verificar que la imagen existe
                if not os.path.exists(imagen_path):
                    messagebox.showerror("Error", "No se puede encontrar la imagen seleccionada")
                    return

                # Guardar la imagen en una ubicación específica
                imagen_destino = self.controlador.guardar_imagen(self.user_id, self.user_name, imagen_path, dedo)

                # Verificar que la imagen se guardó correctamente
                if not os.path.exists(imagen_destino):
                    messagebox.showerror("Error", "Error al guardar la imagen en el destino")
                    return

                # Cargar y mostrar la imagen seleccionada en la interfaz
                try:
                    img = Image.open(imagen_destino)
                    img = img.resize((150, 150))
                    img_tk = ImageTk.PhotoImage(img)
                    label_imagen.config(image=img_tk)
                    label_imagen.image = img_tk
                except Exception as e:
                    messagebox.showerror("Error", f"Error al procesar la imagen con PIL: {str(e)}")
                    return

                # Realizar la predicción del tipo de huella
                try:
                    tipo_huella = predecir_tipo_huella(imagen_destino, model)
                except Exception as e:
                    messagebox.showerror("Error", f"Error en la predicción: {str(e)}")
                    return

                # Encontrar la tarjeta correspondiente
                tarjeta_actual = None
                for tarjeta in self.tarjetas:
                    if tarjeta["label_imagen"] == label_imagen:
                        tarjeta_actual = tarjeta
                        break

                if tarjeta_actual:
                    # Actualizar el tipo de huella
                    tarjeta_actual["imagen_path"] = imagen_destino
                    tarjeta_actual["label_tipo_huella_value"].config(text=tipo_huella)
                    tarjeta_actual["label_tipo_huella"].pack()
                    tarjeta_actual["label_tipo_huella_value"].pack()

                    # Si es presilla o verticilo, abrir FingerprintAnalysis
                    if tipo_huella.lower() in ['presilla', 'verticilo']:
                        def update_label_callback(resultado):
                            if resultado and tarjeta_actual:
                                tarjeta_actual["label_entero"].pack()
                                tarjeta_actual["label_entero_value"].config(text=resultado)
                                tarjeta_actual["label_entero_value"].pack()
                                self.root.update()

                        analysis = FingerprintAnalysis(imagen_destino, update_label_callback, tipo_huella)
                        self.root.wait_window(analysis.root)
                    else:
                        # Si es arco, ocultar los campos de numeración
                        tarjeta_actual["label_entero"].pack_forget()
                        tarjeta_actual["label_entero_value"].pack_forget()

            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar la imagen: {str(e)}")
                print(f"Error detallado: {e}")

    def volver_a_lista(self):
        # Ocultar la vista actual (por ejemplo, la vista de huellas)
        for widget in self.root.winfo_children():
            widget.destroy()  # Destruir todos los widgets actuales en la ventana

        # Importar la vista de la lista de usuarios
        from view.inicio import VistaUsuarios

        # Crear una nueva instancia del controlador (si es necesario)
        controlador = Controlador()

        # Crear y mostrar la vista de usuarios dentro de la misma ventana
        VistaUsuarios(controlador, self.root)  # Pasa la ventana actual para que se actualice

        # Ahora la ventana `self.root` tiene la nueva vista de usuarios.


    def calculos(self):
        # Obtener el comentario del campo de texto
        comentario = self.texto_comentario.get("1.0", tk.END).strip()
        if comentario == "" or comentario == "Escribe aquí tu diagnóstico":
            comentario = None  # Si no se ha escrito un comentario, se guarda como None
        self.controlador.caluarcular(self.user_id, comentario)

    def guardar_datos(self):
        datos_guardados = True
        datos_para_guardar = []

        for tarjeta in self.tarjetas:
            tipo_huella = tarjeta["label_tipo_huella_value"].cget("text")
            imagen_path = tarjeta["imagen_path"]

            if imagen_path:  # Si hay una imagen cargada
                resultado_analisis = tarjeta["label_entero_value"].cget("text")

                # Si el tipo de huella es "arco", no requerimos un conteo
                if tipo_huella.lower() == 'Arco':
                    resultado_analisis = 0  # O puedes dejarlo como None o un valor que indique que no se requiere conteo

                try:
                    # Procesar resultado_analisis solo si no es arco
                    if tipo_huella.lower() != 'arco':
                        if "+" in resultado_analisis:
                            # Si contiene un "+", dividir y sumar ambos valores
                            partes = resultado_analisis.split("+")
                            resultado_analisis = sum(int(parte.strip()) for parte in partes if parte.strip().isdigit())
                        else:
                            # Intentar convertir el resultado a entero directamente
                            resultado_analisis = int(resultado_analisis) if resultado_analisis else 0

                        if resultado_analisis < 0:
                            raise ValueError("El resultado de análisis debe ser un número positivo.")
                    tipo_dedo, mano = tarjeta["label_dedo"].cget("text").split(" ", 1)
                    datos_para_guardar.append({
                        "tipo_huella": tipo_huella,
                        "resultado_analisis": resultado_analisis,
                        "imagen": imagen_path,
                        "mano": mano,
                        "tipo_dedo": tipo_dedo
                    })
                except ValueError:
                    messagebox.showerror("Error",
                                         f"El valor de análisis para {tipo_huella} debe ser un número válido")
                    datos_guardados = False
                    break

        if datos_guardados and datos_para_guardar:
            # Guardar todos los datos
            for dato in datos_para_guardar:
                exito = self.controlador.guardar_datos_huella(
                    self.user_id,
                    dato["tipo_huella"],
                    dato["resultado_analisis"],
                    dato["imagen"],
                    dato["mano"],
                    dato["tipo_dedo"],  # Agregar los parámetros adicionales a guardar en la base de datos, si es necesario
                )
                if not exito:
                    messagebox.showerror("Error",
                                         f"Error al guardar los datos para {dato['tipo_huella']}")
                    return
            self.calculos()  # calculos
            messagebox.showinfo("Éxito", "Datos guardados correctamente")
            # Aquí llamamos al método de actualización de la ventana principal
            #self.root.update()  # Esto puede ayudar a forzar la actualización de la interfaz
            #self.root.destroy()  # Cierra la ventana de tarjetas
            self.root.after(100, self.volver_a_lista)
        else:
            messagebox.showwarning("Advertencia",
                                   "No hay datos completos para guardar o algunos datos son inválidos")


    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Quieres cerrar la aplicación?"):
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)