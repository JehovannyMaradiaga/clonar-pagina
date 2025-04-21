# 🧠 Web Cloner con Inteligencia Artificial

Este proyecto en Python permite **clonar páginas web** incluyendo sus archivos HTML, CSS, JS e imágenes, con un análisis adicional utilizando un modelo de Procesamiento de Lenguaje Natural (NLP). Utiliza **Selenium**, **BeautifulSoup**, **Transformers** y otras herramientas modernas para descargar y analizar sitios web, incluso detectando entidades nombradas dentro del contenido textual de la página.

---

## 🚀 Funcionalidades

- Clonado completo del HTML de una página.
- Descarga automática de archivos CSS, JS e imágenes.
- Procesamiento de imágenes codificadas como `data URI`.
- Análisis de texto con **modelos NLP (Transformers de HuggingFace)**.
- Navegación sin cabeza con Selenium WebDriver.
- Limpieza y sanitización de archivos y directorios.

---

## 📦 Requisitos

Este proyecto requiere Python 3.7 o superior y las siguientes bibliotecas:

- `selenium`
- `webdriver-manager`
- `beautifulsoup4`
- `requests`
- `transformers`
- `Pillow`
- `opencv-python`
- `torch`

---

## ⚙️ Instalación

1. Clona el repositorio o descarga el script.
2. (Opcional) Crea un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Uso
python clonar_pagina.py

Introduce la URL de la página que deseas clonar: https://ejemplo.com

#Autor
Walter Jehovanny Carranza Maradiaga


