import os
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import sys

# Función para obtener la ruta base del entorno actual
def get_base_path():
    if getattr(sys, 'frozen', False):  # Ejecutable PyInstaller
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

# Obtener rutas relativas para el modelo y la imagen
base_path = get_base_path()
ruta_modelo = os.path.join(base_path, 'modelo_huellas_2.keras')
ruta_imagen = os.path.join(base_path,  'arco6.jpg')

# Verificar si el modelo y la imagen existen antes de cargarlos
if not os.path.exists(ruta_modelo):
    print(f"Error: No se encontró el archivo del modelo en '{ruta_modelo}'.")
    sys.exit(1)

if not os.path.exists(ruta_imagen):
    print(f"Error: No se encontró la imagen en '{ruta_imagen}'.")
    sys.exit(1)

# Cargar el modelo entrenado
try:
    model = load_model(ruta_modelo)
    print("Modelo cargado exitosamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    sys.exit(1)

# Función para predecir el tipo de huella dactilar
def predecir_tipo_huella(imagen_path, model):
    try:
        img = image.load_img(imagen_path, target_size=(128, 128))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = model.predict(img_array, verbose=0)
        tipo_huella = np.argmax(prediction, axis=1)

        if tipo_huella == 0:
            return "arco"
        elif tipo_huella == 1:
            return "presilla"
        else:
            return "verticilo"
    except Exception as e:
        raise RuntimeError(f"Error durante la predicción: {e}")

# Intentar realizar la predicción
try:
    tipo_huella = predecir_tipo_huella(ruta_imagen, model)
    print(f'El tipo de huella es: {tipo_huella}')
except Exception as e:
    print(f"Error al procesar la imagen: {e}")

