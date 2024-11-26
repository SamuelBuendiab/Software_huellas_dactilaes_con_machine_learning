import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.draw import line
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class FingerprintAnalysis:
    def __init__(self, img_path, update_label_callback, tipo_huella):
        self.root = tk.Tk()  # Cambiado a Tk() para que solo se abra una ventana principal

        self.root.title("Análisis de Huellas")
        self.root.geometry("900x800")  # Cambia las dimensiones a las que prefieras

        self.img_path = img_path
        self.update_label_callback = update_label_callback
        self.tipo_huella = tipo_huella

        self.red_point = None
        self.green_points = []
        self.conteototal = 0
        self.contador = 0

        self.resultado_final = None

        self.red_point = None
        self.green_points = []
        self.conteo_total = []  # Cambiado a una lista para almacenar conteos individuales


        self.image = cv2.imread(img_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        plt.axis('off')

        # Crear un frame para el fondo azul
        self.header_frame = tk.Frame(self.root, bg="#6098FF")  # Tono azul
        self.header_frame.pack(fill=tk.X)

        # Estilo para el título
        self.title_label = tk.Label(
            self.header_frame,
            text="Conteo de Núcleo a Deltas",
            font=("Arial", 18, "bold"),
            bg="#6098FF",
            fg="black"  # Texto en blanco para contraste
        )
        self.title_label.pack(pady=5)

        # Estilo para el enunciado
        self.instruction_label = tk.Label(
            self.header_frame,
            text="Por favor, presiona con el click izquierdo los deltas y con el click derecho el núcleo de la huella para poder realizar el conteo.",
            wraplength=400,
            font=("Arial", 12),
            bg="#6098FF",
            fg="black"  # Texto en blanco para contraste
        )
        self.instruction_label.pack(pady=5)

        self.fig, self.ax = plt.subplots()
        plt.axis('off')  # Oculta los ejes


        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)

        # Botón con estilo CSS
        self.save_button = tk.Button(self.root, text="Guardar y Salir", command=self.save_and_close)
        self.save_button.pack(pady=10)
        self.style_button(self.save_button)  # Aplicar estilo al botón

        self.root.protocol("WM_DELETE_WINDOW", self.save_and_close)  # Manejar el cierre de la ventana



        self.root.protocol("WM_DELETE_WINDOW", self.save_and_close)  # Manejar el cierre de la ventana

        self.redraw()  # Cargar la imagen al abrir la ventana

    def style_button(self, button):
        button.config(
            bg="#6098FF",  # Color de fondo del botón
            fg="white",  # Color del texto del botón
            font=("Arial", 12, "bold"),
            relief=tk.FLAT,  # Sin relieve
            bd=0  # Sin borde
        )
        button.bind("<Enter>", self.on_enter)
        button.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        event.widget['bg'] = '#007acc'  # Cambiar el color de fondo en hover
        event.widget['fg'] = 'white'

    def on_leave(self, event):
        event.widget['bg'] = '#6098FF'  # Restaurar el color de fondo
        event.widget['fg'] = 'white'

    def onclick(self, event):
        if event.button == 1:  # Click izquierdo para agregar puntos verdes
            # Limitar a un solo punto verde si es "presilla"
            if self.tipo_huella.lower() == "presilla":
                self.green_points = [(event.xdata, event.ydata)]  # Reemplaza cualquier punto verde existente
            else:
                if len(self.green_points) < 2:  # Para "verticilo", permite dos puntos verdes
                    self.green_points.append((event.xdata, event.ydata))
                else:
                    self.green_points.pop(0)
                    self.green_points.append((event.xdata, event.ydata))

        elif event.button == 3:  # Click derecho para el punto rojo (núcleo)
            self.red_point = (event.xdata, event.ydata) if self.red_point is None else None

        self.conteototal = 0
        self.contador = 0
        self.redraw()

    def preprocess_image(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        return binary

    def count_crossed_lines(self, start, end, binary):
        x1, y1 = int(start[0]), int(start[1])
        x2, y2 = int(end[0]), int(end[1])
        rr, cc = line(y1, x1, y2, x2)
        rr = np.clip(rr, 0, binary.shape[0] - 1)
        cc = np.clip(cc, 0, binary.shape[1] - 1)
        intensities = binary[rr, cc]
        crossings = np.sum((intensities[:-1] == 0) & (intensities[1:] == 255))
        self.conteototal += crossings
        self.contador += 1
        return crossings



    def redraw(self):
        self.ax.clear()
        self.ax.imshow(self.image, extent=[0, self.image.shape[1], self.image.shape[0], 0])
        # Configurar límites exactos de la imagen para evitar espacios en blanco
        self.ax.set_xlim(0, self.image.shape[1])
        self.ax.set_ylim(self.image.shape[0], 0)

        for point in self.green_points:
            plt.scatter(point[0], point[1], color='green', s=100)

        if self.red_point is not None:
            plt.scatter(self.red_point[0], self.red_point[1], color='red', s=100)
            binary = self.preprocess_image()

            for green_point in self.green_points:
                plt.plot([self.red_point[0], green_point[0]], [self.red_point[1], green_point[1]], color='blue')
                crossed_count = self.count_crossed_lines(self.red_point, green_point, binary)
                midpoint = ((self.red_point[0] + green_point[0]) / 2, (self.red_point[1] + green_point[1]) / 2)
                plt.text(midpoint[0], midpoint[1], str(crossed_count), color='white', fontweight='bold',
                         bbox=dict(facecolor='blue', alpha=0.5))
                print(f'Línea desde {self.red_point} a {green_point} cruza {crossed_count} crestas blancas. '
                      f'Conteo total: {self.conteototal}')

            self.conteo_total = []  # Reiniciar conteo total en cada redibujo
            for green_point in self.green_points:
                crossed_count = self.count_crossed_lines(self.red_point, green_point, binary)
                self.conteo_total.append(crossed_count)  # Agregar conteo a la lista
                plt.plot([self.red_point[0], green_point[0]], [self.red_point[1], green_point[1]], color='blue')

                # Calcular el punto medio para mostrar el conteo
                midpoint = ((self.red_point[0] + green_point[0]) / 2, (self.red_point[1] + green_point[1]) / 2)
                plt.text(midpoint[0], midpoint[1], str(crossed_count), color='white', fontweight='bold',
                         bbox=dict(facecolor='blue', alpha=0.5))
                print(f'Línea desde {self.red_point} a {green_point} cruza {crossed_count} crestas blancas.')


        plt.axis('off')
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.canvas.draw()

    def save_and_close(self):

        # Llamar al callback para actualizar el label en la clase que llama
        self.update_label_callback(self.conteototal)  # Actualiza la variable en VistaHuellas

        # Cerrar solo la ventana de análisis
        self.root.destroy()

# Ejemplo de uso
#if __name__ == "__main__":
#    img_path = 'pres5.png'  # Ruta de la imagen a analizar
#   analysis = FingerprintAnalysis(img_path)
#    analysis.run()

        if self.conteo_total:  # Verificar que hay conteos
            # Formar el resultado como una cadena con los conteos separados por '+'
            self.resultado_final = " + ".join(map(str, self.conteo_total))

            # Mostrar un mensaje de confirmación
            messagebox.showinfo("Éxito", f"Se contaron {self.resultado_final} crestas")

            # Llamar al callback con el resultado
            if self.update_label_callback:
                self.update_label_callback(self.resultado_final)
        else:
            messagebox.showwarning("Advertencia", "No se ha realizado ningún conteo")
            return

        self.root.destroy()


# Callback para actualizar el conteo total en una etiqueta (o simplemente imprimirlo)
def update_label_callback(conteo_total):
    print(f"Conteo total de crestas cruzadas: {conteo_total}")
    # Ahora, creas la instancia pasando todos los parámetros







