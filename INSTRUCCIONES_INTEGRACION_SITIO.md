# 🌐 Integración de Dmente Scraper en www.dmentedigital.co

## OPCIÓN: EMBEBIDA EN IFRAME (0 Costos)

---

## ✅ PASO 1: Deploy en Streamlit Cloud (5 minutos)

### 1.1 Preparar Repositorio GitHub

```bash
# En tu carpeta del proyecto
git init
git add .
git commit -m "Dmente Scraper Pro v2.0 - Initial deploy"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/dmente-scraper-pro.git
git push -u origin main
```

### 1.2 Ir a https://share.streamlit.io/

1. Haz clic en "Deploy an app"
2. Conecta tu GitHub
3. Selecciona:
   - Repository: `dmente-scraper-pro`
   - Branch: `main`
   - Main file path: `app.py`
4. Click "Deploy"

**Espera 2-3 minutos** → Tu app estará en:
```
https://dmentedigital-dmente-scraper-pro-xyzabc.streamlit.app
```

---

## ✅ PASO 2: Integrar en tu Sitio Web

### 2.1 Opción A: Página Dedicada (Recomendado)

Crea archivo en tu sitio: `/herramientas/scraper.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dmente Scraper Pro - Herramienta de Web Scraping</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Plus Jakarta Sans', Arial, sans-serif;
            background: linear-gradient(135deg, #061421 0%, #0a1c2e 100%);
            color: #f8fafc;
            min-height: 100vh;
        }

        .header {
            background: rgba(43, 235, 210, 0.05);
            border-bottom: 1px solid rgba(43, 235, 210, 0.15);
            padding: 2rem 1rem;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #2bebd2 0%, #089ca0 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .header p {
            color: rgba(248, 250, 252, 0.6);
            font-size: 1.1rem;
            margin-bottom: 1rem;
        }

        .badge {
            display: inline-block;
            background: rgba(43, 235, 210, 0.12);
            border: 1px solid rgba(43, 235, 210, 0.3);
            color: #2bebd2;
            padding: 0.4rem 0.8rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }

        .feature-card {
            background: rgba(43, 235, 210, 0.03);
            border: 1px solid rgba(43, 235, 210, 0.15);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }

        .feature-card:hover {
            border-color: rgba(43, 235, 210, 0.3);
            box-shadow: 0 8px 32px rgba(43, 235, 210, 0.06);
        }

        .feature-card h3 {
            color: #2bebd2;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }

        .feature-card p {
            color: rgba(248, 250, 252, 0.6);
            font-size: 0.95rem;
            line-height: 1.5;
        }

        .app-container {
            background: rgba(6, 20, 33, 0.8);
            border: 1px solid rgba(43, 235, 210, 0.15);
            border-radius: 16px;
            overflow: hidden;
            margin: 2rem 0;
            box-shadow: 0 8px 32px rgba(43, 235, 210, 0.06);
        }

        iframe {
            width: 100%;
            height: 900px;
            border: none;
            display: block;
        }

        .footer {
            text-align: center;
            padding: 2rem;
            border-top: 1px solid rgba(43, 235, 210, 0.08);
            color: rgba(248, 250, 252, 0.5);
            font-size: 0.9rem;
        }

        .footer a {
            color: #2bebd2;
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8rem;
            }

            iframe {
                height: 600px;
            }

            .features {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <span class="badge">⚡ Herramienta Gratuita</span>
        <h1>🧠 Dmente Scraper Pro</h1>
        <p>Extracción profesional de datos web</p>
        <p style="font-size: 0.9rem; color: rgba(248, 250, 252, 0.4);">
            "No es azar, es propósito"
        </p>
    </div>

    <div class="container">
        <div class="features">
            <div class="feature-card">
                <h3>🎭 Motores Múltiples</h3>
                <p>Playwright, Selenium y BeautifulSoup integrados para máxima flexibilidad</p>
            </div>
            <div class="feature-card">
                <h3>📊 Exportación Flexible</h3>
                <p>Descarga resultados en CSV, Excel o JSON compatible con APIs</p>
            </div>
            <div class="feature-card">
                <h3>🔐 Seguro y Ético</h3>
                <p>Autenticación integrada, pausas aleatorias y manejo de rate limits</p>
            </div>
            <div class="feature-card">
                <h3>⚡ Tiempo Real</h3>
                <p>Consola en vivo con logs color-coded y estadísticas instantáneas</p>
            </div>
            <div class="feature-card">
                <h3>🧠 Inteligente</h3>
                <p>Auto-detección de estructura de página para mejor precisión</p>
            </div>
            <div class="feature-card">
                <h3>👤 Multi-usuario</h3>
                <p>Sistema de login integrado para roles admin y operador</p>
            </div>
        </div>

        <div class="app-container">
            <iframe 
                src="https://dmentedigital-dmente-scraper-pro-XXXXX.streamlit.app" 
                title="Dmente Scraper Pro">
            </iframe>
        </div>
    </div>

    <div class="footer">
        <p>
            Desarrollado por <a href="https://www.dmentedigital.co">Dmente Digital</a> 
            | Ingeniería de Crecimiento Digital
        </p>
        <p style="margin-top: 1rem; font-size: 0.85rem;">
            © 2026 Dmente Digital. Todos los derechos reservados.
        </p>
    </div>
</body>
</html>
```

### 2.2 Opción B: Página HTML Simplificada

```html
<html>
<head>
    <title>Dmente Scraper Pro</title>
</head>
<body>
    <h1>🧠 Dmente Scraper Pro</h1>
    <p>Herramienta profesional de web scraping</p>
    
    <iframe 
        src="https://dmentedigital-dmente-scraper-pro-XXXXX.streamlit.app" 
        width="100%" 
        height="900"
        style="border: none;">
    </iframe>
</body>
</html>
```

---

## 🔗 PASO 3: Configurar en tu Sitio Web

### Opción 1: WordPress

1. Ir a Pages → New Page
2. Título: "Dmente Scraper Pro"
3. Agregar bloque "HTML personalizado"
4. Pegar el código del iframe
5. Publicar

### Opción 2: Sitio HTML Estático

1. Crear carpeta `/herramientas/`
2. Crear archivo `/herramientas/scraper.html`
3. Pegar el código HTML completo arriba
4. Subir al servidor
5. URL: `www.dmentedigital.co/herramientas/scraper`

### Opción 3: Sitios Web (Wix, Squarespace, etc.)

1. Ir a editor → Agregar "Insertar código"
2. Copiar el iframe:
```html
<iframe 
    src="https://dmentedigital-dmente-scraper-pro-XXXXX.streamlit.app" 
    width="100%" 
    height="900"
    style="border: none;">
</iframe>
```

---

## ⚠️ IMPORTANTE: Reemplazar la URL

**Tu URL exacta será:**
```
https://dmentedigital-dmente-scraper-pro-[CODIGO_UNICO].streamlit.app
```

Reemplaza `XXXXX` en todos los ejemplos con el código real que recibirás de Streamlit Cloud.

---

## 📊 Costo Total

| Item | Costo |
|------|-------|
| Streamlit Cloud | **GRATIS** |
| Hosting en tu sitio | **GRATIS** |
| Dominio | Ya tienes |
| **TOTAL** | **0€** |

---

## 📈 Beneficios para Dmente Digital

✅ **Lead Magnet Gratuito**
- Captar leads cualificados
- Demostrar capacidades técnicas

✅ **Diferenciación Competitiva**
- Herramienta exclusiva
- Atrae empresas que necesitan scraping

✅ **SEO Benefit**
- Página indexable en Google
- Palabra clave: "web scraping tool"

✅ **Integración Perfecta**
- Mantiene branding de Dmente
- Colores y tipografía consistent

---

## 🚨 Requisitos Previos

Antes de publicar, asegúrate de:

- [ ] Cambiar contraseñas por defecto en `users.json`
- [ ] Crear `.env` con variables de entorno
- [ ] Actualizar `.gitignore`
- [ ] Testing local completo

Ver: `RECOMENDACIONES_FINALES.txt`

---

## 📞 Soporte

Si tienes dudas en la integración:
1. Verificar URL correcta de Streamlit Cloud
2. Revisar que iframe no esté bloqueado por CORS
3. Probar en navegador privado

**¿Listo? Adelante con el deploy! 🚀**
