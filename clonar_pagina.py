import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import urllib.parse
import re
from PIL import Image
import numpy as np
import base64
import cv2  # OpenCV para análisis de imágenes
from transformers import pipeline  # Para procesamiento NLP (ejemplo)

# Inicialización del modelo NLP para extraer texto
nlp_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# Función para iniciar el navegador con webdriver-manager
def iniciar_navegador():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Ejecutar en modo sin cabeza
    options.add_argument('--disable-gpu')  # Desactivar GPU para eficiencia
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

# Función para obtener el contenido HTML de la página
def obtener_contenido_html(url):
    navegador = iniciar_navegador()
    navegador.get(url)
    html = navegador.page_source
    navegador.quit()
    return html

# Función para guardar el HTML de la página
def guardar_html(soup, directorio_destino):
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)  # Crear el directorio si no existe
    with open(os.path.join(directorio_destino, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(str(soup))

# Función para descargar archivos CSS, JS o imágenes
def descargar_archivo(url, base_url, directorio_destino):
    archivo_url = urllib.parse.urljoin(base_url, url)
    nombre_archivo = os.path.basename(archivo_url)
    nombre_archivo = limpiar_nombre_archivo(nombre_archivo)  # Sanitizar el nombre del archivo

    # Asegurarse de que el directorio de destino existe
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    try:
        respuesta = requests.get(archivo_url)
        respuesta.raise_for_status()
        with open(os.path.join(directorio_destino, nombre_archivo), 'wb') as f:
            f.write(respuesta.content)
        print(f"Archivo {nombre_archivo} descargado exitosamente.")
    except requests.exceptions.RequestException as e:
        print(f"No se pudo descargar {nombre_archivo}: {e}")

# Función para guardar data URIs (imágenes, CSS, JS, etc.)
def guardar_data_uri(data_uri, directorio_destino):
    try:
        # Identificar el tipo de contenido (por ejemplo, image/png)
        tipo_contenido, datos_base64 = data_uri.split(',', 1)
        
        # Decodificar el contenido base64
        contenido_binario = base64.b64decode(datos_base64)

        # Definir un nombre de archivo único para la data URI
        nombre_archivo = 'data_uri_' + str(hash(data_uri)) + '.' + obtener_extension(tipo_contenido)
        
        # Guardar el archivo en el directorio de destino
        with open(os.path.join(directorio_destino, nombre_archivo), 'wb') as f:
            f.write(contenido_binario)
        print(f"Data URI guardada como {nombre_archivo}.")
    except Exception as e:
        print(f"Error al guardar la data URI: {e}")

# Función para obtener la extensión del archivo de acuerdo al tipo MIME
def obtener_extension(tipo_contenido):
    if 'image' in tipo_contenido:
        if 'png' in tipo_contenido:
            return 'png'
        elif 'jpeg' in tipo_contenido:
            return 'jpg'
        elif 'gif' in tipo_contenido:
            return 'gif'
    elif 'css' in tipo_contenido:
        return 'css'
    elif 'javascript' in tipo_contenido:
        return 'js'
    return 'bin'

# Función para limpiar el nombre del archivo (quitar caracteres no válidos)
def limpiar_nombre_archivo(nombre):
    # Limitar la longitud del nombre del archivo
    nombre = nombre[:200]  # Limitar a 200 caracteres para evitar nombres demasiado largos

    # Reemplazar caracteres no válidos
    nombre = re.sub(r'[<>:"/\\|?*]', '_', nombre)  # Reemplazar caracteres no válidos
    nombre = re.sub(r'\s+', '_', nombre)  # Reemplazar espacios con guiones bajos
    return nombre

# Función para clonar la página web con IA y procesamiento NLP
def clonar_pagina(url):
    print(f"Clonando {url}...")

    # Obtener el contenido HTML de la página
    html = obtener_contenido_html(url)
    soup = BeautifulSoup(html, 'html.parser')

    # Análisis con NLP (Extracción de contenido textual para comprender mejor la estructura)
    texto = " ".join([p.get_text() for p in soup.find_all('p')])
    entidades = nlp_model(texto)
    print(f"Entidades identificadas en el texto de la página: {entidades}")

    # Crear la carpeta para guardar los archivos
    base_url = urllib.parse.urlparse(url).netloc
    directorio_destino = base_url.replace('.', '_')  # Sanitización del nombre del directorio
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)

    # Guardar el HTML de la página
    guardar_html(soup, directorio_destino)

    # Descargar archivos CSS y JS
    for tag in soup.find_all(['link', 'script']):
        if tag.name == 'link' and tag.get('rel') == ['stylesheet']:
            href = tag.get('href')
            if href:
                descargar_archivo(href, url, directorio_destino)
        elif tag.name == 'script' and tag.get('src'):
            src = tag.get('src')
            if src:
                descargar_archivo(src, url, directorio_destino)

    # Descargar imágenes y procesarlas para replicar estilo visual
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            if src.startswith('data:'):
                # Si la URL es una data URI, la procesamos
                guardar_data_uri(src, directorio_destino)
            else:
                # Si no es una data URI, descargamos el archivo normalmente
                descargar_archivo(src, url, directorio_destino)

    print(f"Página clonada y guardada en la carpeta: {directorio_destino}")

# Ingreso de URL y ejecución
if __name__ == "__main__":
    while True:
        url = input("Introduce la URL de la página que deseas clonar: ")
        clonar_pagina(url)
        
        # Preguntar si desea continuar o salir
        opcion = input("¿Deseas clonar otra página? (s/n): ").lower()
        if opcion != 's':
            print("Saliendo del programa.")
            break
