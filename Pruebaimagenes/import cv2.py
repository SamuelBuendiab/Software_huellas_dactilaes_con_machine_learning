import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model

# Cargar el modelo entrenado
model = load_model('C:/Users/User/Documents/Pruebaimagenes/modelo_huellas_2.keras')

# Función para predecir el tipo de huella dactilar
def predecir_tipo_huella(imagen_path, model):
    img = image.load_img(imagen_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    prediction = model.predict(img_array)
    tipo_huella = np.argmax(prediction, axis=1)[0]
    
    if tipo_huella == 0:
        return "Arco"
    elif tipo_huella == 1:
        return "Presilla"
    else:
        return "Verticilo"

# Función para detectar el núcleo y los deltas
def detectar_nucleo_deltas(imagen_path, tipo_huella):
    img = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.equalizeHist(img)  # Mejorar el contraste
    
    # Aplicar múltiples filtros de Gabor para resaltar las crestas
    orientations = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    filtered_imgs = []
    for theta in orientations:
        g_kernel = cv2.getGaborKernel((21, 21), 8.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
        filtered_img = cv2.filter2D(img, cv2.CV_8UC3, g_kernel)
        filtered_imgs.append(filtered_img)
    
    combined_img = np.max(filtered_imgs, axis=0)
    
    # Detectar los puntos singulares usando Harris corner detection
    corners = cv2.goodFeaturesToTrack(combined_img, maxCorners=10, qualityLevel=0.01, minDistance=10)
    corners = np.intp(corners)
    
    # Clasificar los puntos como núcleo o deltas basándose en su posición
    centro_x, centro_y = img.shape[1] // 2, img.shape[0] // 2
    distancias = [(x, y, np.sqrt((x - centro_x)**2 + (y - centro_y)**2)) for (x, y) in [corner.ravel() for corner in corners]]
    distancias.sort(key=lambda x: x[2])
    
    # El punto más cercano al centro es el núcleo
    nucleo = distancias[0]
    
    # Determinar el número de deltas según el tipo de huella
    deltas = []
    if tipo_huella == "Presilla":
        deltas = [distancias[1]]
    elif tipo_huella == "Verticilo":
        deltas = [distancias[1], distancias[2]]
    
    return nucleo, deltas

# Función para detectar minutiae
def detectar_minutiae(binary_img):
    minutiae_terminaciones = []
    minutiae_bifurcaciones = []

    # Esqueletonización usando morfología
    size = np.size(binary_img)
    skel = np.zeros(binary_img.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False
    
    while not done:
        eroded = cv2.erode(binary_img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(binary_img, temp)
        skel = cv2.bitwise_or(skel, temp)
        binary_img = eroded.copy()

        zeros = size - cv2.countNonZero(binary_img)
        if zeros == size:
            done = True

    rows, cols = skel.shape
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if skel[i, j] == 255:
                neighbors = [skel[i + x, j + y] for x in [-1, 0, 1] for y in [-1, 0, 1] if not (x == 0 and y == 0)]
                if neighbors.count(255) == 1:
                    minutiae_terminaciones.append((j, i))
                elif neighbors.count(255) == 3:
                    minutiae_bifurcaciones.append((j, i))
    
    return minutiae_terminaciones, minutiae_bifurcaciones

# Función para contar las crestas entre el núcleo y los deltas usando minutiae
def contar_crestas_con_minutiae(imagen_path, nucleo, deltas):
    img = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.equalizeHist(img)  # Mejorar el contraste
    
    # Aplicar un filtro de Gabor para resaltar las crestas
    g_kernel = cv2.getGaborKernel((21, 21), 8.0, np.pi / 2, 10.0, 0.5, 0, ktype=cv2.CV_32F)
    filtered_img = cv2.filter2D(img, cv2.CV_8UC3, g_kernel)
    
    # Usar adaptive thresholding para binarizar la imagen
    binary_img = cv2.adaptiveThreshold(filtered_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Detectar minutiae
    terminaciones, bifurcaciones = detectar_minutiae(binary_img)
    
    # Contar las crestas entre el núcleo y cada delta
    nucleo_x, nucleo_y = nucleo[0], nucleo[1]
    conteos = []
    for delta in deltas:
        delta_x, delta_y = delta[0], delta[1]
        conteo_crestas = 0
        for terminacion in terminaciones:
            t_x, t_y = terminacion
            if min(nucleo_x, delta_x) <= t_x <= max(nucleo_x, delta_x) and min(nucleo_y, delta_y) <= t_y <= max(nucleo_y, delta_y):
                conteo_crestas += 1
        conteos.append(conteo_crestas)
    
    return conteos

# Ejemplo de uso
imagen_path = r"C:\Users\User\Documents\Pruebaimagenes\press4.png"
tipo_huella = predecir_tipo_huella(imagen_path, model)
print(f'El tipo de huella es: {tipo_huella}')

nucleo, deltas = detectar_nucleo_deltas(imagen_path, tipo_huella)
print(f'Núcleo detectado en: {nucleo[:2]}')
print(f'Deltas detectados en: {[delta[:2] for delta in deltas]}')

conteos_crestas = contar_crestas_con_minutiae(imagen_path, nucleo, deltas)
for i, conteo in enumerate(conteos_crestas):
    print(f'Número de crestas desde el núcleo hasta el delta {i + 1}: {conteo}')
