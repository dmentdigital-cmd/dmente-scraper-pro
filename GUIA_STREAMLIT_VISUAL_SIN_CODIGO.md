# 🚀 GUÍA VISUAL: PUBLICAR EN STREAMLIT CLOUD
## Sin código, solo clics

---

## 📝 CREDENCIALES NUEVAS (Guardar en lugar seguro)

```
👤 USUARIO ADMIN:
   Usuario: admin
   Contraseña: Dmente2026!Admin@Secure

👤 USUARIO OPERADOR:
   Usuario: dmente
   Contraseña: Scraper2026!Operador@Pro
```

**⚠️ IMPORTANTE:** Guarda estas contraseñas en un lugar seguro (nota, Password Manager, etc.)

---

## PASO 1: CREAR REPOSITORIO EN GITHUB

### Paso 1.1: Ir a GitHub

1. Abre navegador: **https://github.com**
2. Si tienes cuenta, da clic en **Sign In**
3. Si no tienes cuenta, da clic en **Sign up**

### Paso 1.2: Crear Nuevo Repositorio

```
En la esquina superior derecha:
┌─────────────────────┐
│ Perfil ▼            │
│ └─ New repository   │ ← DA CLIC AQUÍ
│ └─ Your repositories│
│ └─ Settings         │
└─────────────────────┘
```

### Paso 1.3: Llenar Formulario

```
Repository name:
┌─────────────────────────────────────────┐
│ dmente-scraper-pro                      │
└─────────────────────────────────────────┘

Description:
┌─────────────────────────────────────────┐
│ Professional web scraping tool          │
└─────────────────────────────────────────┘

☑ Public (importante para Streamlit Cloud)
☐ Private

☑ Add a README file

Crear repositorio → DA CLIC EN "Create repository"
```

### Paso 1.4: Subir Tu Código

En tu computadora, abre Terminal/Cmd en la carpeta `webscraping-main`:

```bash
git init
git add .
git commit -m "Initial commit: Dmente Scraper Pro v2.0"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/dmente-scraper-pro.git
git push -u origin main
```

**Espera a que termine (2-3 minutos)**

---

## PASO 2: PUBLICAR EN STREAMLIT CLOUD

### Paso 2.1: Ir a Streamlit Cloud

1. Abre navegador: **https://share.streamlit.io/**

2. Ves esta pantalla:
```
┌──────────────────────────────────────────────┐
│        🎈 Streamlit Community Cloud          │
│                                              │
│  [Sign up with GitHub]  [Already have app?] │
└──────────────────────────────────────────────┘
```

3. Da clic en **Sign up with GitHub**

### Paso 2.2: Autorizar GitHub

1. Se abre ventana GitHub
2. Autoriza Streamlit a acceder a tu GitHub
3. Selecciona solo el repositorio `dmente-scraper-pro`
4. Da clic en **Authorize**

### Paso 2.3: Deploy Automático

Después de autorizar, ves:

```
┌──────────────────────────────────────────────┐
│  🚀 Deploy an app                            │
│                                              │
│  Repository:                                 │
│  ┌────────────────────────────────────────┐  │
│  │ TU_USUARIO/dmente-scraper-pro ▼       │  │ ← SELECCIONAR
│  └────────────────────────────────────────┘  │
│                                              │
│  Branch:                                     │
│  ┌────────────────────────────────────────┐  │
│  │ main ▼                                 │  │ ← SELECCIONAR
│  └────────────────────────────────────────┘  │
│                                              │
│  Main file path:                             │
│  ┌────────────────────────────────────────┐  │
│  │ app.py                                 │  │ ← DEBE ESTAR CORRECTA
│  └────────────────────────────────────────┘  │
│                                              │
│  [Deploy]                                    │ ← DA CLIC
└──────────────────────────────────────────────┘
```

### Paso 2.4: Esperar Deploy

Verás pantalla de carga:
```
┌──────────────────────────────────────────────┐
│                                              │
│  🔄 Installing dependencies...               │
│                                              │
│  ⏳ Please wait... (2-3 minutos)              │
│                                              │
│  Progreso:                                   │
│  ████████████░░░░░░░░░  50%                 │
│                                              │
└──────────────────────────────────────────────┘
```

**ESPERA ENTRE 2-3 MINUTOS** ⏰

### Paso 2.5: ¡LISTO! 🎉

Cuando termine, verás:

```
┌──────────────────────────────────────────────┐
│  ✅ App is running                           │
│                                              │
│  Your app is available at:                   │
│  https://dmentedigital-dmente-scraper-pro... │
│  -XXXXXXXXXXXXXXXXXXXX.streamlit.app/        │
│                                              │
│  [Copy URL] [Open in new tab]                │
└──────────────────────────────────────────────┘
```

**Copia la URL** y guárdala. Esa es tu aplicación pública.

---

## PASO 3: PROBAR LA APP

1. Da clic en **Open in new tab** (o pega la URL en navegador)

2. Verás pantalla de login:
```
┌────────────────────────────────────┐
│         🧠 Dmente Scraper Pro     │
│                                    │
│  👤 Usuario:                       │
│  [                              ]  │
│                                    │
│  🔒 Contraseña:                    │
│  [                              ]  │
│                                    │
│  [🚀 Iniciar Sesión]               │
└────────────────────────────────────┘
```

3. Ingresa:
   - Usuario: `admin`
   - Contraseña: `Dmente2026!Admin@Secure`

4. Verás la aplicación funcionando ✅

---

## PASO 4: INTEGRAR EN TU SITIO WEB

### Opción A: Si Tienes WordPress

1. Ve a: **Pages → Add New**
2. Título: "Dmente Scraper Pro"
3. Arriba, da clic en los **3 puntos** y selecciona **Code Editor**

```
Pega esto en el código:

<iframe 
    src="https://dmentedigital-dmente-scraper-pro-XXXXX.streamlit.app" 
    width="100%" 
    height="900"
    style="border: none; display: block;">
</iframe>
```

Reemplaza `XXXXX` con el código que te dio Streamlit.

4. Guarda y publica

### Opción B: Si Tienes Wix

1. Ve a editor de tu sitio
2. Arriba a la izquierda: **Add → Embed → Custom Embed**

```
Pega este código:

<iframe 
    src="https://dmentedigital-dmente-scraper-pro-XXXXX.streamlit.app" 
    width="100%" 
    height="900"
    style="border: none;">
</iframe>
```

3. Guarda

### Opción C: Si Tienes Otro Editor Web

Busca opción como:
- "Embed Code"
- "HTML"
- "Custom Code"
- "Iframe"

Y pega:
```
<iframe 
    src="https://dmentedigital-dmente-scraper-pro-XXXXX.streamlit.app" 
    width="100%" 
    height="900"
    style="border: none;">
</iframe>
```

---

## ✅ CHECKLIST FINAL

- [ ] Archivo `users.json` actualizado (ya hecho)
- [ ] Archivo `.env` creado (ya hecho)
- [ ] Archivo `.gitignore` creado (ya hecho)
- [ ] Repositorio GitHub creado
- [ ] Código subido a GitHub (git push)
- [ ] App publicada en Streamlit Cloud
- [ ] App integrada en tu sitio web
- [ ] Probaste login con nuevas credenciales
- [ ] Compartiste URL con clientes

---

## 🆘 SI ALGO NO FUNCIONA

### "No puedo subir código a GitHub"

Abre Terminal/Cmd y copia esto (en la carpeta webscraping-main):

```
git config --global user.email "tu@email.com"
git config --global user.name "Tu Nombre"
git init
git add .
git commit -m "Dmente Scraper Pro"
git branch -M main
git remote add origin https://github.com/TUNOMBRE/dmente-scraper-pro.git
git push -u origin main
```

### "Streamlit no inicia el deploy"

1. Verifica que el archivo se llama exactamente `app.py`
2. Verifica que está en la carpeta raíz (no en subcarpeta)
3. Intenta de nuevo

### "El login no funciona"

Las contraseñas son:
- Usuario: `admin` | Contraseña: `Dmente2026!Admin@Secure`
- Usuario: `dmente` | Contraseña: `Scraper2026!Operador@Pro`

---

## 📞 RESUMEN

✅ **Costo:** $0
✅ **Tiempo:** 30-40 minutos
✅ **Resultado:** App pública en www.dmentedigital.co/herramientas/scraper
✅ **Usuarios:** Ilimitados

---

## SIGUIENTE PASO

Cuando hayas terminado, tienes:

1. ✅ App funcionando en Streamlit Cloud
2. ✅ Integrada en tu sitio web
3. ✅ Credenciales seguras
4. ✅ **LISTO PARA CAPTAR LEADS**

**¿Necesitas ayuda? Contacta a Dmente Digital**

"No es azar, es propósito"
www.dmentedigital.co
