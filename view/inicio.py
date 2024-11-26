import tkinter as tk
from model.dbConnetion import conectar
from tkinter import ttk, messagebox, filedialog
from tkinter.filedialog import asksaveasfilename
from view.viewUser import VistaUsuario
from view.viewShowPrints import VistaHuellasUsuario
from controller.listController import Controlador
import re
from tkcalendar import DateEntry
import tkinter.simpledialog as simpledialog


class VistaUsuarios:
    def __init__(self, controlador, root=None):
        self.conexion = conectar()
        self.controlador = controlador
        self.root = root or tk.Tk()
        self.root.title("Gestión de Usuario")
        self.root.state("zoomed")
        self.root.configure(bg="#e6f7ff")  # Fondo azul cielo


        # Frame superior con el título
        header_frame = tk.Frame(self.root, bg="#87CEEB")  # Fondo azul más oscuro
        header_frame.pack(fill=tk.X)

        titulo = tk.Label(header_frame, text="Gestión de Usuario", font=("Verdana Bold", 30), fg="white", bg="#87CEEB")
        titulo.pack(padx=20, pady=10)

        # Frame para los botones, ordenados verticalmente
        botones_frame = tk.Frame(self.root, bg="#e6f7ff")
        botones_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        # Crear botones con estilo personalizado
        self.boton_exportar = self.crear_boton(botones_frame, "Exportar ", self.exportar_base_datos)
        self.boton_agregar = self.crear_boton(botones_frame, "Agregar Cliente", self.agregar_cliente)
        self.boton_reporte = self.crear_boton(botones_frame, "Reporte por fecha", self.reporte)

        # Frame para la barra de búsqueda
        search_frame = tk.Frame(self.root, bg="#e6f7ff")
        search_frame.pack(pady=10)  # Espaciado vertical

        # Etiqueta para la barra de búsqueda
        search_label = tk.Label(search_frame, text="Buscar:", font=("Verdana", 12), bg="#e6f7ff")
        search_label.pack(side=tk.LEFT, padx=5)

        # Entry para la búsqueda
        self.search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        # Botón de búsqueda
        self.search_button = tk.Button(search_frame, text="Buscar", command=self.buscar_usuario, bg="#5bbce4",
                                       fg="white", font=("Arial", 12))
        self.search_button.pack(side=tk.LEFT, padx=5)

        # Vincular eventos de hover y leave al botón
        self.search_button.bind("<Enter>", self.on_hover)
        self.search_button.bind("<Leave>", self.on_leave)

        self.after_id = None  # Inicializar el ID de 'after'

        # Frame para la tabla y scrollbar
        table_frame = tk.Frame(self.root)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Scrollbar para la tabla
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Frame para la tabla y scrollbar
        table_frame = tk.Frame(self.root)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Scrollbar para la tabla
        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configuración de las columnas, agregando las nuevas columnas
        self.tabla = ttk.Treeview(table_frame, columns=(
        "ID", "Nombre", "Grupo", "Correo", "Cedula", "Número Celular", "Edad", "Genero","Fecha", "Editar", "Borrar"),
                                  show="headings", yscrollcommand=scrollbar.set)

        # Encabezado con evento de clic para ordenar, agregando los nuevos campos
        self.tabla.heading("ID", text="ID Usuario", command=lambda: self.ordenar_columna("ID"))
        self.tabla.heading("Nombre", text="Nombre", command=lambda: self.ordenar_columna("Nombre"))
        self.tabla.heading("Grupo", text="Grupo", command=lambda: self.ordenar_columna("Grupo"))
        self.tabla.heading("Correo", text="Correo", command=lambda: self.ordenar_columna("Correo"))
        self.tabla.heading("Cedula", text="Cedula", command=lambda: self.ordenar_columna("Cedula"))
        self.tabla.heading("Número Celular", text="Número Celular",
                           command=lambda: self.ordenar_columna("Número Celular"))
        self.tabla.heading("Edad", text="Edad", command=lambda: self.ordenar_columna("Edad"))
        self.tabla.heading("Genero", text="Genero", command=lambda: self.ordenar_columna("Genero"))
        self.tabla.heading("Fecha", text="Fecha", command=lambda: self.ordenar_columna("Fecha"))
        self.tabla.heading("Editar", text="Editar")
        self.tabla.heading("Borrar", text="Borrar")

        # Configuración de columnas
        self.tabla.column("ID", width=100, anchor=tk.CENTER)
        self.tabla.column("Nombre", width=150, anchor=tk.W)
        self.tabla.column("Grupo", width=150, anchor=tk.W)
        self.tabla.column("Correo", width=200, anchor=tk.W)
        self.tabla.column("Cedula", width=150, anchor=tk.CENTER)
        self.tabla.column("Número Celular", width=150, anchor=tk.CENTER)
        self.tabla.column("Edad", width=150, anchor=tk.CENTER)  # Ajusta el ancho si es necesario
        self.tabla.column("Genero", width=150, anchor=tk.CENTER)  # Ajusta el ancho si es necesario
        self.tabla.column("Fecha", width=150, anchor=tk.CENTER)
        self.tabla.column("Editar", width=80, anchor=tk.CENTER)
        self.tabla.column("Borrar", width=80, anchor=tk.CENTER)

        # Scroll de la tabla
        scrollbar.config(command=self.tabla.yview)

        # Estilos para encabezado y filas
        style = ttk.Style(self.root)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="white", foreground="black", rowheight=35)
        style.configure("Treeview", rowheight=30, font=("Arial", 12))


        self.tabla.tag_configure("oddrow", background="#e6f7ff")  # Fondo azul cielo para filas impares
        self.tabla.tag_configure("evenrow", background="#ccf2ff")  # Azul claro para filas pares

        # Evento para cambiar el color de las filas al pasar el mouse
        self.tabla.bind('<Motion>', self.on_mouse_over_row)

        # Evento para seleccionar fila y abrir vista de huellas
        self.tabla.bind("<Double-1>", self.seleccionar_usuario)

        # Inserción de la tabla en el frame
        self.tabla.pack(fill=tk.BOTH, expand=True)

        # Variable para recordar la última fila sobre la que se pasó el mouse
        self.previous_row = None

        self.cargar_usuarios()

        # Asignar el evento de clic para la tabla
        self.tabla.bind("<Button-1>", self.on_click)

    # Actualización de cargar_usuarios para incluir los nuevos campos
    def cargar_usuarios(self):
        usuarios = self.controlador.obtener_usuarios()
        for index, usuario in enumerate(usuarios):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            # Incluye los nuevos campos en la lista de valores a insertar en cada fila
            self.tabla.insert("", tk.END, values=(*usuario, "Editar", "Borrar"), tags=(tag,))

    def on_click(self, event):
        """Detecta si se hizo clic en el botón de editar o borrar y ejecuta la acción correspondiente."""
        region = self.tabla.identify("region", event.x, event.y)
        if region == "cell":  # Solo procede si se hace clic en una celda
            item_id = self.tabla.identify_row(event.y)
            column = self.tabla.identify_column(event.x)

            if item_id:
                if column == "#10":  # Columna "Editar"
                    self.editar_usuario(item_id)
                elif column == "#11":  # Columna "Borrar"
                    self.borrar_usuario(item_id)

    import tkinter as tk
    from tkinter import ttk

    def editar_usuario(self, item_id):
        """Abre la vista de edición para el usuario seleccionado."""
        usuario = self.tabla.item(item_id, "values")
        user_id = usuario[0]  # ID del usuario

        # Crear una ventana para editar
        edit_window = tk.Toplevel(self.root)
        edit_window.title(f"Editar Usuario - ID: {user_id}")

        # Configurar color de fondo de la ventana
        edit_window.configure(bg="#ADD8E6")  # Fondo azul claro

        # Definir el tamaño y centrar la ventana
        width, height = 350,450  # Tamaño de la ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        edit_window.geometry(f"{width}x{height}+{x}+{y}")

        edit_window.grab_set()

        # Crear un Frame dentro de la ventana para contener el formulario
        form_frame = tk.Frame(edit_window, bg="#ffffff")  # Fondo blanco para el formulario
        form_frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

        # Asegurar que los labels y entries no se corten
        form_frame.columnconfigure(0, weight=1)
        form_frame.columnconfigure(1, weight=2)

        # Campos de edición dentro del Frame
        tk.Label(form_frame, text="Nombre:", bg="#ffffff").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        nombre_entry = tk.Entry(form_frame, width=30)
        nombre_entry.grid(row=0, column=1, padx=10, pady=10)
        nombre_entry.insert(0, usuario[1])

        tk.Label(form_frame, text="Grupo:", bg="#ffffff").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        grupo_entry = tk.Entry(form_frame, width=30)
        grupo_entry.grid(row=1, column=1, padx=10, pady=10)
        grupo_entry.insert(0, usuario[2])

        tk.Label(form_frame, text="Correo:", bg="#ffffff").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        correo_entry = tk.Entry(form_frame, width=30)
        correo_entry.grid(row=2, column=1, padx=10, pady=10)
        correo_entry.insert(0, usuario[3])

        tk.Label(form_frame, text="Cédula:", bg="#ffffff").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        numero_id_entry = tk.Entry(form_frame, width=30)
        numero_id_entry.grid(row=3, column=1, padx=10, pady=10)
        numero_id_entry.insert(0, usuario[4])

        tk.Label(form_frame, text="Celular:", bg="#ffffff").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        numero_celular_entry = tk.Entry(form_frame, width=30)
        numero_celular_entry.grid(row=4, column=1, padx=10, pady=10)
        numero_celular_entry.insert(0, usuario[5])

        tk.Label(form_frame, text="Edad:", bg="#ffffff").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        edad_entry = tk.Entry(form_frame, width=30)
        edad_entry.grid(row=5, column=1, padx=10, pady=10)
        edad_entry.insert(0, usuario[6])

        tk.Label(form_frame, text="Género:", bg="#ffffff").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        genero_combo = ttk.Combobox(form_frame, values=["Masculino", "Femenino"], width=28, state="readonly")
        genero_combo.grid(row=6, column=1, padx=10, pady=10)
        genero_combo.set(usuario[7])

        # Botón para guardar cambios dentro del Frame
        guardar_button=tk.Button(form_frame, text="Guardar", bg="#33a4d2", fg="white",borderwidth=0, height=2, width=8,
                  command=lambda: self.guardar_edicion(user_id, nombre_entry.get(), grupo_entry.get(),
                                                       correo_entry.get(), numero_id_entry.get(),
                                                       numero_celular_entry.get(), edad_entry.get(), genero_combo.get(),
                                                       edit_window))
        guardar_button.grid(row=7, columnspan=2, pady=20)

        # Cambiar color al pasar el mouse
        guardar_button.bind("<Enter>", lambda e: guardar_button.config(bg="#e3f2f9", fg="black"))
        guardar_button.bind("<Leave>", lambda e: guardar_button.config(bg="#33a4d2", fg="white"))


    def validar_correo(self, correo):
        return "@" in correo and "." in correo

    def validar_nombre(self, nombre):
        return bool(re.match(r"^[A-Za-z\s]+$", nombre))

    def validar_numero(self, valor):
        return valor.isdigit()


    def guardar_edicion(self, user_id, nombre, grupo, correo, numero_id, numero_celular, edad,genero, edit_window):
        # Validación para evitar que los campos "Nombre" y "Correo" queden en blanco
        if not nombre.strip():
            messagebox.showerror("Error", "El campo 'Nombre' no puede estar en blanco.")
            return False
        if not grupo.strip():
            messagebox.showerror("Error", "El campo 'Grupo' no puede estar en blanco.")
            return False
        if not correo.strip():
            messagebox.showerror("Error", "El campo 'Correo' no puede estar en blanco.")
            return False
        if not numero_id.strip():
            messagebox.showerror("Error", "El campo 'Cedula' no puede estar en blanco.")
            return False
        if not numero_celular.strip():
            messagebox.showerror("Error", "El campo 'Numero celular' no puede estar en blanco.")
            return False
        if not edad.strip():
            messagebox.showerror("Error", "El campo 'Edad' no puede estar en blanco.")
            return False


        # Validación de formato de los campos
        if not self.validar_nombre(nombre):
            messagebox.showerror("Error", "El nombre debe contener solo letras y espacios..")
            return False
        if not grupo.isalpha():
            messagebox.showerror("Error", "El nombre debe contener solo letras.")
            return False
        if not numero_id.isdigit():
            messagebox.showerror("Error", "La cédula debe ser un número.")
            return False
        if not numero_celular.isdigit():
            messagebox.showerror("Error", "El número de celular debe ser un número.")
            return False
        if not edad.isdigit():
            messagebox.showerror("Error", "La edad debe ser un número.")
            return False
        # Validación del correo electrónico
        if "@" not in correo or "." not in correo:
            messagebox.showerror("Error", "El correo debe contener '@' y un punto ('.').")
            return False


        # Lógica para actualizar en la base de datos
        resultado = self.controlador.actualizar_usuario(user_id, grupo, nombre, correo, numero_id, numero_celular,edad,genero)
        if resultado is True:
            messagebox.showinfo("Éxito", "Usuario actualizado correctamente.")
            edit_window.destroy()

            # Actualizar la tabla después de la edición
            self.tabla.delete(*self.tabla.get_children())  # Limpiar la tabla
            self.cargar_usuarios()  # Recargar los usuarios
            self.previous_row = None
        elif resultado is False:
            messagebox.showerror("Error", "No se pudo actualizar el usuario.")
            self.previous_row = None
        else:
            # En caso de que resultado sea None o algún valor inesperado
            print("Error: La función actualizar_usuario no devolvió un valor esperado.")
            messagebox.showerror("Error", "Ocurrió un error inesperado al intentar actualizar el usuario.")
            self.previous_row = None

    def borrar_usuario(self, item_id):
        """ Elimina al usuario seleccionado después de confirmación. """
        usuario = self.tabla.item(item_id, "values")
        user_id = usuario[0]
        nombre_paciente = usuario[1]

        confirm = messagebox.askyesno("Confirmar Borrar", f"¿Estás seguro de que deseas eliminar a {nombre_paciente}?")
        if confirm:
            self.controlador.eliminar_usuario(user_id)
            self.tabla.delete(item_id)
            messagebox.showinfo("Usuario Borrado", f"Usuario {nombre_paciente} ha sido eliminado.")

            self.previous_row = None

    def reporte(self):
        # Crear una ventana para editar la fecha y hora de ingreso
        edit_window = tk.Toplevel(self.root,bg="white")

        # Definir el tamaño y centrar la ventana
        width, height = 550, 150  # Tamaño de la ventana ampliado para incluir los nuevos widgets
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        edit_window.geometry(f"{width}x{height}+{x}+{y}")

        # Selector de fecha para la fecha de inicio
        tk.Label(edit_window, text="Fecha de Inicio:",bg="white").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        fecha_inicio = DateEntry(edit_window, date_pattern='yyyy-MM-dd')
        fecha_inicio.grid(row=0, column=1, padx=10, pady=10)

        # Selector de hora para la fecha de inicio
        tk.Label(edit_window, text="Hora de Inicio (HH:MM):",bg="white").grid(row=0, column=2, padx=10, pady=10, sticky="e")
        hora_inicio = ttk.Spinbox(edit_window, from_=0, to=23, wrap=True, width=2, format='%02.0f')
        hora_inicio.grid(row=0, column=3, padx=(0, 5), pady=10)
        hora_inicio.set('00')  # Valor inicial

        minuto_inicio = ttk.Spinbox(edit_window, from_=0, to=59, wrap=True, width=2, format='%02.0f')
        minuto_inicio.grid(row=0, column=4, padx=(0, 5), pady=10)
        minuto_inicio.set('00')  # Valor inicial

        # Selector de fecha para la fecha de fin
        tk.Label(edit_window, text="Fecha de Fin (Opcional):",bg="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        fecha_fin = DateEntry(edit_window, date_pattern='yyyy-MM-dd')
        fecha_fin.grid(row=1, column=1, padx=10, pady=10)

        # Selector de hora para la fecha de fin
        tk.Label(edit_window, text="Hora de Fin (HH:MM):",bg="white").grid(row=1, column=2, padx=10, pady=10, sticky="e")
        hora_fin = ttk.Spinbox(edit_window, from_=0, to=23, wrap=True, width=2, format='%02.0f')
        hora_fin.grid(row=1, column=3, padx=(0, 5), pady=10)
        hora_fin.set('00')  # Valor inicial

        minuto_fin = ttk.Spinbox(edit_window, from_=0, to=59, wrap=True, width=2, format='%02.0f')
        minuto_fin.grid(row=1, column=4, padx=(0, 5), pady=10)
        minuto_fin.set('00')  # Valor inicial

        def guardar_reporte():
            # Obtener las fechas y horas seleccionadas
            fecha_hora_inicio = f"{fecha_inicio.get()} {hora_inicio.get()}:{minuto_inicio.get()}:00"
            fecha_hora_fin = None

            # Si la fecha de fin está seleccionada, la formateamos
            if fecha_fin.get_date():
                fecha_hora_fin = f"{fecha_fin.get()} {hora_fin.get()}:{minuto_fin.get()}:00"

            # Expresión regular para validar el formato de fecha y hora SQL
            fecha_hora_regex = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"

            # Validar el formato de la fecha de inicio
            if not re.match(fecha_hora_regex, fecha_hora_inicio):
                messagebox.showerror("Error", "El formato de la fecha y hora de inicio no es válido.")
                return

            # Abrir una ventana para seleccionar dónde guardar el informe
            archivo_destino = asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf")],
                title="Guardar reporte como"
            )

            # Si el usuario seleccionó una ubicación
            if archivo_destino:
                # Llamar a reporte_guardar en el controlador para que guarde el reporte en el archivo destino
                self.controlador.reporte_guardar(fecha_hora_inicio, fecha_hora_fin, archivo_destino)
                messagebox.showinfo("Éxito", "Se ha guardado con éxito el reporte")
                edit_window.destroy()

        # Botón para guardar el reporte
        guardar_reporte_button = tk.Button(edit_window, text="Guardar Reporte", bg="#33a4d2", fg="white", borderwidth=0,
                                           height=2, width=13,
                                           command=guardar_reporte)
        guardar_reporte_button.grid(row=2, columnspan=5, pady=20)

        # Cambiar color al pasar el mouse
        guardar_reporte_button.bind("<Enter>", lambda e: guardar_reporte_button.config(bg="#e3f2f9", fg="black"))
        guardar_reporte_button.bind("<Leave>", lambda e: guardar_reporte_button.config(bg="#33a4d2", fg="white"))

    def crear_boton(self, parent, text, command):
        button = tk.Button(parent, text=text, command=command, height=2, width=20, bg="#5bbce4", fg="white", borderwidth=0)
        button.bind("<Enter>", self.on_hover)
        button.bind("<Leave>", self.on_leave)
        button.pack(fill=tk.X, padx=5, pady=5)

        return button

    def agregar_cliente(self):
        self.root.withdraw()
        nuevo_root = tk.Toplevel(self.root)
        VistaUsuario(nuevo_root, self.root)

    #def importar_sql(self):
        #try:
            #archivo = filedialog.askopenfilename(filetypes=[("SQL Files", "*.sql")])
            #if archivo:
                # Leer el archivo SQL y ejecutar las consultas
                #with open(archivo, 'r', encoding='utf-8') as sql_file:
                    #sql_script = sql_file.read()

                #resultado = self.controlador.ejecutar_script_sql(sql_script)

                #if resultado:
                    #messagebox.showinfo("Éxito", "Base de datos importada correctamente")
                    # Actualizar la tabla con los nuevos datos
                    #self.tabla.delete(*self.tabla.get_children())
                    #self.cargar_usuarios()
                #else:
                    #messagebox.showerror("Error", "Error al importar la base de datos")
        #except Exception as e:
            #messagebox.showerror("Error", f"Error al importar: {str(e)}")

    def exportar_base_datos(self):
        try:
            # Pedir al usuario el nombre del grupo
            grupo = simpledialog.askstring(
                title="Formulario de Exportación",
                prompt="Ingrese el nombre del grupo para exportar:",
                initialvalue="",
                parent=None
            )

            if not grupo:
                messagebox.showwarning("Advertencia", "No se ha ingresado un grupo.")
                return

            # Verificar si el grupo existe en la base de datos
            cursor = self.conexion.cursor()
            query_grupo = """
                   SELECT DISTINCT grupo
                   FROM user
                   WHERE grupo = ?
               """
            cursor.execute(query_grupo, (grupo,))
            grupo_existe = cursor.fetchone()

            if not grupo_existe:
                messagebox.showwarning("Advertencia", f"El grupo '{grupo}' no existe.")
                cursor.close()
                return

            # Llamamos a la función que exporta los datos a Excel
            archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",  # Cambiar la extensión a .xlsx
                filetypes=[("Excel Files", "*.xlsx")]
            )

            if archivo:

                resultado = self.controlador.exportar_a_excel(archivo,grupo)

                if resultado:
                    messagebox.showinfo("Éxito", "Datos exportados a Excel correctamente")
                else:
                    messagebox.showinfo("Exportación completada", "Aviso: algunos dedos no tienen huella cargada.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def on_hover(self, event):
        self.after_id = self.root.after(200, self.change_color, event)

    def change_color(self, event):
        event.widget.config(bg="white", fg="#5bbce4") # Fondo blanco y texto azul cielo

    def on_leave(self, event):
        self.root.after_cancel(self.after_id)  # Cancelar la acción de cambio de color si se sale del botón
        event.widget.config(bg="#5bbce4", fg="white")  # Volver al color original

    def on_mouse_over_row(self, event):
        """ Cambia el fondo de la fila sobre la que pasa el mouse, sin afectar el encabezado. """
        row_id = self.tabla.identify_row(event.y)

        # Restaurar color de la fila anterior solo si previous_row es válido
        if self.previous_row and self.tabla.exists(self.previous_row):
            tag = self.tabla.item(self.previous_row, "tags")[0]
            if tag == "oddrow":
                self.tabla.tag_configure(self.previous_row, background="#e6f7ff")
            else:
                self.tabla.tag_configure(self.previous_row, background="#ccf2ff")

        # Cambiar el color de la fila actual
        if row_id:  # Asegurarse de que no es el encabezado
            self.tabla.tag_configure(row_id, background="#cceeff")  # Azul muy suave
            self.previous_row = row_id  # Guardar la fila actual

    def ordenar_columna(self, col):
        """ Ordena la tabla por la columna especificada. """
        # Obtener datos de la tabla
        data = [(self.tabla.item(item)["values"], item) for item in self.tabla.get_children()]
        data.sort(key=lambda x: x[0][self.tabla["columns"].index(col)])  # Ordenar por el valor de la columna

        # Limpiar la tabla actual y volver a insertar los datos ordenados
        self.tabla.delete(*self.tabla.get_children())
        for index, (values, item) in enumerate(data):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            self.tabla.insert("", tk.END, values=values, tags=(tag,))

        # Resetear previous_row
        self.previous_row = None

    def seleccionar_usuario(self, event):
        """ Maneja la selección de un usuario de la tabla y abre la vista de huellas. """
        selected_item = self.tabla.selection()
        if selected_item:
            user_id = self.tabla.item(selected_item, "values")[0]  # Obtener el ID del usuario
            nombre_paciente = self.tabla.item(selected_item, "values")[1]  # Obtener el nombre del usuario (asumiendo que es el segundo valor)
            print(f"Usuario seleccionado: ID={user_id}, Nombre={nombre_paciente}")
            self.abrir_vista_huellas(user_id, nombre_paciente)

    def abrir_vista_huellas(self, user_id, nombre_paciente):
        """Abre la vista de huellas para el usuario seleccionado."""
        self.root.withdraw()  # Oculta la ventana principal
        nuevo_root = tk.Toplevel(self.root)
        nuevo_root.state("zoomed")
        VistaHuellasUsuario(nuevo_root, user_id, nombre_paciente, self.root) # Pasar referencia a la ventana de usuarios

    def buscar_usuario(self):
        search_term = self.search_entry.get().lower()  # Obtener el texto de búsqueda
        self.tabla.delete(*self.tabla.get_children())  # Limpiar la tabla actual
        usuarios = self.controlador.obtener_usuarios()  # Obtener la lista de usuarios

        for index, usuario in enumerate(usuarios):
            # Verificar si el término de búsqueda está en alguno de los campos
            if (search_term in str(usuario[0]).lower() or  # ID
                    search_term in usuario[1].lower() or # Nombre
                    search_term in usuario[2].lower() or # Grupo
                    search_term in usuario[3].lower() or  # Correo
                    search_term in str(usuario[4]).lower() or  # Número ID
                    search_term in str(usuario[5]).lower()):  # Número Celular
                tag = 'oddrow' if index % 2 == 0 else 'evenrow'
                self.tabla.insert("", tk.END, values=(*usuario, "Editar", "Borrar"),tags=(tag,))  # Insertar el usuario en la tabla

        # Resetear previous_row después de la búsqueda
        self.previous_row = None

    def on_closing(self):
        if messagebox.askokcancel("Salir", "¿Quieres cerrar la aplicación?"):
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)




if __name__ == "__main__":
    controlador = Controlador()  # Asegúrate de tener tu controlador inicializado
    app = VistaUsuarios(controlador)
    app.root.mainloop()