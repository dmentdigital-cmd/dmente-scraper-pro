@echo off
chcp 65001 >nul
title 🧠 Dmente Scraper Pro - Iniciando...

echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║  🧠 DMENTE DIGITAL - Scraper Pro v2.0                   ║
echo  ║  "No es azar, es propósito"                             ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.

:: Check Python
echo [1/4] Verificando Python...
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ ERROR: Python no encontrado. Instálalo desde python.org
    pause
    exit /b 1
)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do echo     ✅ Python %%v detectado

:: Check dependencies
echo.
echo [2/4] Verificando dependencias...
pip show streamlit >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo     📦 Instalando dependencias...
    pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo ❌ ERROR al instalar dependencias.
        pause
        exit /b 1
    )
) else (
    echo     ✅ Dependencias verificadas
)

:: Check Playwright browsers
echo.
echo [3/4] Verificando navegadores Playwright...
python -c "from playwright.sync_api import sync_playwright" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo     📦 Instalando Playwright...
    pip install playwright
    playwright install chromium
) else (
    echo     ✅ Playwright listo
)

:: Launch
echo.
echo [4/4] 🚀 Lanzando Dmente Scraper Pro...
echo.
echo     🌐 Abriendo en: http://localhost:8501
echo     Para detener: presiona Ctrl+C
echo.
streamlit run app.py

pause
