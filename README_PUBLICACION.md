# 🧠 Dmente Scraper Pro v2.0
## Herramienta Profesional de Extracción de Datos Web

> *"No es azar, es propósito."*  
> **Dmente Digital** — Ingeniería de Crecimiento Digital

---

## 📊 Estado del Proyecto

**✅ Listo para Publicación**

Esta aplicación ha sido evaluada y aprobada para deployment en ambiente de producción.

---

## 🚀 Publicación Rápida (Streamlit Cloud)

### En 5 Minutos:

1. **Crear repositorio GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Dmente Scraper Pro v2.0"
   git push -u origin main
   ```

2. **Ir a https://share.streamlit.io/**

3. **Seleccionar:**
   - Repositorio: `dmente-scraper-pro`
   - Rama: `main`
   - Archivo: `app.py`

4. **Deploy automático en 2 minutos**

**URL Pública:** `https://dmentedigital-scraper.streamlit.app`

---

## 🔐 Seguridad - ANTES de Publicar

### ⚠️ URGENTE (Hacer ahora):

1. **Cambiar contraseñas por defecto:**
   ```json
   {
     "admin": {
       "password_hash": "TU_NUEVO_HASH_AQUI"
     },
     "dmente": {
       "password_hash": "TU_NUEVO_HASH_AQUI"
     }
   }
   ```

2. **Crear archivo `.env`:**
   ```
   STREAMLIT_SERVER_PORT=8501
   STREAMLIT_SERVER_HEADLESS=true
   STREAMLIT_LOGGER_LEVEL=info
   ```

3. **Actualizar `.gitignore`:**
   ```
   .env
   users.json
   scraping_history.json
   __pycache__/
   ```

### Muy Recomendado:

- [ ] Implementar rate limiting (máx 5 scrapes/minuto)
- [ ] Agregar logging de auditoría
- [ ] Validar URLs (evitar localhost, privadas)
- [ ] Sanitizar selectores CSS

---

## 📦 Requisitos de Deployments

| Opción | Costo | Tiempo | Ventajas |
|--------|-------|--------|----------|
| **Streamlit Cloud** | Gratis | 2 min | Fácil, rápido, HTTPS automático |
| **DigitalOcean** | $5/mes | 30 min | Control total, mejor rendimiento |
| **Heroku** | $7/mes | 20 min | Simple, escalable |

**Recomendación:** Streamlit Cloud para inicio rápido.

---

## 🏗️ Arquitectura

```
webscraping-main/
├── app.py                    # 🎯 Interfaz Streamlit
├── engine/
│   ├── scraper.py           # ⚙️ Motor de scraping unificado
│   └── __init__.py
├── .streamlit/
│   └── config.toml          # 🎨 Configuración de tema
├── requirements.txt         # 📦 Dependencias
├── users.json              # 👥 Base de datos de usuarios
├── scraping_history.json   # 📜 Historial de ejecuciones
└── resultados/             # 💾 Datos exportados
```

---

## 🔧 Stack Tecnológico

- **Backend:** Python 3.12+
- **Frontend:** Streamlit 1.30+
- **Navegadores:** Playwright, Selenium, BeautifulSoup4
- **Datos:** Pandas, OpenPyXL
- **Autenticación:** SHA256 (nativa)

---

## 📋 Funcionalidades

### Motores de Scraping
- ✅ **Playwright** (Recomendado) — Navegador moderno
- ✅ **Selenium** — Automatización robusta
- ✅ **BeautifulSoup4** — Parsing estático rápido

### Modos de Operación
- 📜 Scroll infinito
- 🔐 Login + Extracción
- 📄 Página estática
- 📚 Paginación múltiple

### Exportación de Datos
- 📄 CSV (universal)
- 📊 Excel (.xlsx)
- 🔗 JSON (API-friendly)

---

## 👥 Usuarios por Defecto

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| `admin` | `DmenteDigital2026!` | Administrador |
| `dmente` | `scraper2026` | Operador |

**⚠️ Cambiar inmediatamente en producción**

---

## 📊 Estadísticas de Proyecto

- **Líneas de código:** ~1000+
- **Dependencias:** 9 principales
- **Tiempo de desarrollo:** Curso Platzi + iteraciones
- **Versión actual:** v2.0 (Producción)

---

## 🚦 Pasos Finales (Checklist)

- [ ] Cambiar contraseñas por defecto
- [ ] Crear archivo .env
- [ ] Actualizar .gitignore
- [ ] Crear repositorio GitHub
- [ ] Configurar Streamlit Cloud
- [ ] Probar en staging
- [ ] Publicar URL
- [ ] Monitorear logs
- [ ] Implementar backups

---

## 📞 Soporte y Contacto

**Dmente Digital**  
🌐 www.dmentedigital.co  
📧 dmentedigital@gmail.com  
💡 Slogan: *"No es azar, es propósito"*

---

## 📜 Licencia

Uso interno de Dmente Digital. Todos los derechos reservados.

---

**Última actualización:** Abril 2026  
**Estado:** ✅ Aprobado para Publicación
