# Especificaciones Técnicas: Herramienta de Web Scraping Profesional - Dmente Digital

## 1. Visión General
El objetivo es transformar los scripts de Python (Selenium y Playwright) desarrollados durante el curso en una aplicación funcional con interfaz gráfica (GUI). La herramienta debe permitir a un usuario no técnico ejecutar procesos de scraping, monitorear el progreso y descargar los resultados en Excel/CSV de manera profesional.

**Lema del Proyecto:** "No es azar, es propósito."

## 2. Interfaz de Usuario (UI/UX) Requerida
La interfaz debe ser limpia, moderna y fácil de usar, inspirada en herramientas de automatización de alto nivel.

- **Panel de Control:** - Input para URL objetivo.
    - Botones de acción: [Iniciar Scraping], [Detener], [Limpiar Datos].
- **Configuración de Navegación:**
    - Toggle para "Ver Proceso" (Modo No-Headless) o "Segundo Plano" (Headless).
    - Selector de "Profundidad de Scroll" (Número de veces que el bot bajará).
- **Consola de Estado:** Visualización de mensajes en tiempo real (ej: "🚀 Iniciando sesión...", "✅ Datos extraídos correctamente").
- **Tabla de Resultados:** Vista previa de los datos capturados antes de descargar.

## 3. Lógica y Funcionalidades Core (Reglas de Negocio)
Basado en las mejores prácticas de **Dmente Digital**, el desarrollador debe asegurar:

- **Gestión Automática de Drivers:** Implementar `webdriver-manager` para Selenium y `playwright install` para evitar errores de versión de Chrome.
- **Protocolo de Scroll Infinito:** Realizar desplazamientos con un delay de 5 segundos para asegurar la carga completa de elementos dinámicos.
- **Extracción Híbrida:** Utilizar la potencia de interacción de Selenium/Playwright y la limpieza de `BeautifulSoup` para obtener texto puro sin basura HTML.
- **Manejo de Errores (Resiliencia):** - Control de **Error 429** (Too Many Requests) mediante pausas aleatorias.
    - Manejo de excepciones para que la app no se cierre si falla una carga.
- **Exportación:** Generar un archivo **CSV** universal al finalizar cada tarea.

## 4. Requerimientos para Antigravity
1. **Unificar Scripts:** Tomar los archivos `.py` del curso y centralizar la lógica en un solo motor de ejecución.
2. **Entorno de Ejecución:** Asegurar compatibilidad con Python 3.12.
3. **Librerías Clave:** `selenium`, `playwright`, `beautifulsoup4`, `webdriver-manager`, `pandas` (para el CSV) y un framework de interfaz (como `Streamlit`, `CustomTkinter` o `Flet`).

## 5. Instrucciones de Entrega
La aplicación final debe ser ejecutable sin que el usuario tenga que editar el código. Debe incluir un botón de "Descargar Resultados" que entregue la información lista para ser procesada por el equipo estratégico.
