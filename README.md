# 🧠 Dmente Scraper Pro v2.0

**Herramienta profesional de extracción de datos web** desarrollada por [Dmente Digital](http://dmentedigital.co/).

> *"No es azar, es propósito."*

---

## 📋 Descripción General

Aplicación de **Web Scraping** con interfaz gráfica premium que unifica los scripts de Selenium, Playwright y BeautifulSoup en un solo motor de ejecución. Permite a un usuario no técnico extraer datos de sitios web, monitorear el progreso en tiempo real y descargar resultados en CSV/Excel.

---

## ✨ Funcionalidades Principales

| Característica | Detalle |
|---|---|
| **3 Motores** | Playwright (recomendado), Selenium + WebDriver, Requests + BS4 |
| **4 Modos** | Scroll Infinito, Login + Extracción, Página Estática, Paginación Múltiple |
| **Auto-detección** | Reconoce automáticamente la estructura de la página (citas, productos, tablas, etc.) |
| **Consola en Tiempo Real** | Log con mensajes color-coded y timestamps |
| **Exportación** | Descarga directa en CSV y Excel (.xlsx) |
| **Resiliencia** | Manejo de Error 429, pausas aleatorias, reintentos éticos |
| **Selector CSS** | Permite personalizar qué elementos extraer |
| **Headless/Visible** | Toggle para ejecutar en segundo plano o ver el navegador |

---

## 🔧 Requisitos Técnicos

- **Python 3.12+**
- **Google Chrome** (para motores con navegador)
- **Sistema Operativo**: Windows 10/11

### Librerías Principales
- `streamlit` — Interfaz gráfica
- `playwright` — Automatización moderna de navegador
- `selenium` + `webdriver-manager` — Automatización legacy
- `beautifulsoup4` — Parsing HTML
- `pandas` + `openpyxl` — Procesamiento y exportación de datos

---

## 🚀 Instalación y Ejecución

### Opción 1: Doble clic (Recomendado)
```
📂 Abrir carpeta del proyecto
→ Doble clic en: iniciar_scraper.bat
```

### Opción 2: Manual
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Instalar navegador de Playwright
playwright install chromium

# 3. Lanzar la aplicación
streamlit run app.py
```

La aplicación se abrirá automáticamente en: **http://localhost:8501**

---

## 📁 Estructura del Proyecto

```
webscraping-main/
├── app.py                         # 🎯 Aplicación principal (Streamlit GUI)
├── iniciar_scraper.bat            # 🚀 Lanzador automático
├── requirements.txt               # 📦 Dependencias Python
├── .streamlit/
│   └── config.toml                # 🎨 Tema Dark Tech (Dmente Digital)
├── engine/
│   ├── __init__.py
│   └── scraper.py                 # ⚙️ Motor unificado de scraping
├── resultados/                    # 💾 Archivos exportados
│   ├── productos_multi.csv
│   ├── productos_eticos.csv
│   └── ...
├── 0__instalación.ipynb           # 📓 Notebooks del curso (referencia)
├── 1__mi_primer_scraper.ipynb
├── 2__paginación_y_múltiples_páginas.ipynb
├── 3__página_interactiva.ipynb
├── 4__scroll_infinito.ipynb
├── 5__formulario.ipynb
├── 6__página_interactiva_playwright.py
├── 7__scroll_infinito_playwright.py
├── 8__formulario_playwright_1.py
└── 8__formulario_playwright_2.py
```

---

## 💡 Ejemplos de Uso

### Scraping con Scroll Infinito
1. URL: `http://quotes.toscrape.com/scroll`
2. Motor: Playwright
3. Modo: Scroll Infinito
4. Profundidad: 5
5. Click "🚀 Iniciar Scraping"

### Scraping con Login
1. URL: `http://quotes.toscrape.com/scroll`
2. Modo: Login + Extracción
3. Usuario: `platzi-admin` / Contraseña: `12345`
4. Click "🚀 Iniciar Scraping"

### Paginación Múltiple
1. URL: `http://books.toscrape.com/catalogue/category/books_1/page-{}.html`
2. Motor: Requests + BS4
3. Modo: Paginación Múltiple
4. Páginas: 5
5. Click "🚀 Iniciar Scraping"

---

## 🏗️ Desarrollado por

**[Dmente Digital](http://dmentedigital.co/)** — Ingeniería de Crecimiento Digital  
*No es azar, es propósito.*
