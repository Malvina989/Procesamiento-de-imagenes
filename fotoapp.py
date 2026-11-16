# Instalamos las bibliotecas
# pip install opencv-python pillow numpy matplotlib

# Importamos bibliotecas
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter, ImageOps                                            
# import skimage.io as io 
# from skimage.color import rgb2gray

#from google.colab import drive
#drive.mount('/content/drive')

# Comprobamos versiones
# print("OpenCV:", cv2.__version__)
# print("Pillow:", Image.__version__)

# Ruta de las img guardadas
#folder = "/content/drive/MyDrive/UPSO/ProcesamientoImg/"

def menu():

  print("==================\n BIENVENIDOS A FOTOAPP \n=================")

  # Cargar y redimensionar img
  ruta = input("Ingrese la ruta de la imagen: ")

  plataforma = input(
      "Ingrese la plataforma (Youtube, Instagram, Twitter o Facebook): "
  )

  imagen = redimensionar(ruta, plataforma)

  print("\nImagen cargada y redimensionada correctamente.")

  # Menú de operaciones
  while True:

      print("\n========== MENÚ PRINCIPAL ==========")
      print("1 - Mostrar imagen redimensionada")
      print("2 - Ajustar contraste")
      print("3 - Aplicar filtros")
      print("4 - Resaltar bordes y contornos")
      print("5 - Salir")

      try:
          opcion = int(input("\nSeleccione una opción: "))

          if opcion == 1:

              imagen.show()

          elif opcion == 2:

              ajustar_contraste(imagen)

          elif opcion == 3:

              aplicar_filtro(imagen)

          elif opcion == 4:

              resaltar_bordes(imagen)

          elif opcion == 5:

              print("Gracias por utilizar el programa.")
              break

          else:
              print("Opción incorrecta. Intente nuevamente.")

      except ValueError as error:
          print("Error:", error)

      except Exception as error:
          print("Ocurrió un error:", error)

# Función para abrir foto con Pillow y redimensionarla según elección del usuario
def redimensionar(ruta, plataforma):

  # Diccionario con opciones y medidas
  dimensiones = {
  "youtube": (1280, 720), # Miniatura Youtube
  "instagram": (1080, 1440), # Instagram
  "twitter": (1024, 412), # X (Twitter)
  "facebook": (1080, 1080) # Facebook formato cuadrado
}
  
  # Validamos que la plataforma esté entre las opciones
  plataforma = plataforma.lower()

  while plataforma not in dimensiones:
      plataforma = input(
          "Ingrese una plataforma disponible: Youtube, Instagram, Twitter o Facebook: "
      ).lower()

  # Validamos la ruta de la imagen
  while True:
      try:
          imagen = Image.open(ruta)
          break

      except FileNotFoundError:
          print("No se encontró la imagen.")
          ruta = input("Ingrese nuevamente la ruta: ")

  # Tomamos dimensiones de destino
  nuevo_ancho, nuevo_alto = dimensiones[plataforma]

  # Redimensionamos sin deformar
  img_resize = ImageOps.pad(imagen, (nuevo_ancho, nuevo_alto), color=(255, 255, 255))

  return img_resize

# Función para ajustar contraste utilizando histograma
# La imagen ya esta cargada
def ajustar_contraste(imagen):

    if imagen is None:
        raise ValueError("Primero debe cargar una imagen.")

    # Convertimos a escala de grises
    img = imagen.convert("L")

    # Convertimos a array de NumPy
    imgbyn = np.array(img)

    # Ecualizamos el histograma
    equ = cv2.equalizeHist(imgbyn)

    # Mostramos imagen original y ecualizada
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(imgbyn, cmap="gray")
    plt.title("Imagen original")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(equ, cmap="gray")
    plt.title("Imagen ecualizada")
    plt.axis("off")

    plt.savefig("resultado.png")
    plt.show()
    plt.close()

# Función para aplicar filtros  
def aplicar_filtro(imagen):

  if imagen is None:
      raise ValueError("Primero debe cargar una imagen.")

  filtros = {
      1: ("Blur", ImageFilter.BLUR),
      2: ("Contour", ImageFilter.CONTOUR),
      3: ("Detail", ImageFilter.DETAIL),
      4: ("Edge Enhance", ImageFilter.EDGE_ENHANCE),
      5: ("Edge Enhance More", ImageFilter.EDGE_ENHANCE_MORE),
      6: ("Emboss", ImageFilter.EMBOSS),
      7: ("Find Edges", ImageFilter.FIND_EDGES),
      8: ("Sharpen", ImageFilter.SHARPEN),
      9: ("Smooth", ImageFilter.SMOOTH)
  }

  opcion = 0

  while opcion not in filtros:
      print("\nSeleccione un filtro:")

      for numero, (nombre, filtro) in filtros.items():
          print(numero, "-", nombre)

      try:
          opcion = int(input("Ingrese el número del filtro: "))

          if opcion not in filtros:
              print("Opción incorrecta. Intente nuevamente.")

      except ValueError:
          print("Debe ingresar un número.")

  nombre_filtro, filtro = filtros[opcion]

  img_filtrada = imagen.filter(filtro)

  plt.figure(figsize=(10, 5))

  plt.subplot(1, 2, 1)
  plt.imshow(imagen)
  plt.title("Imagen original")
  plt.axis("off")

  plt.subplot(1, 2, 2)
  plt.imshow(img_filtrada)
  plt.title(nombre_filtro)
  plt.axis("off")

  nombre_archivo = nombre_filtro.lower().replace(" ", "_") + ".png"

  plt.savefig(nombre_archivo)
  plt.show()
  plt.close()

  return img_filtrada
  
def resaltar_bordes(imagen):

  # Convertimos a escala de grises
  img = imagen.convert("L")

  # Convertimos a array de NumPy
  imgbyn = np.array(img)

  # Umbralización de Otsu
  umbral, binaria = cv2.threshold(
      imgbyn, 0, 255,
      cv2.THRESH_BINARY + cv2.THRESH_OTSU
  )

  # Detección de bordes con Canny
  canny = cv2.Canny(imgbyn, 100, 200)

  # Mostrar resultados
  plt.figure(figsize=(12, 4))

  plt.subplot(1, 3, 1)
  plt.imshow(imagen)
  plt.title("Imagen original")
  plt.axis("off")

  plt.subplot(1, 3, 2)
  plt.imshow(binaria, cmap="gray")
  plt.title("Umbralización Otsu")
  plt.axis("off")

  plt.subplot(1, 3, 3)
  plt.imshow(canny, cmap="gray")
  plt.title("Bordes Canny")
  plt.axis("off")

  plt.tight_layout()
  plt.show()

  return binaria, canny



    
