"""
╔══════════════════════════════════════════════════════════════╗
║   🔍 DMENTE DIGITAL - Flexible Lead Scraper                 ║
║   "No es azar, es propósito"                                ║
║   Búsqueda Inteligente Multi-Sector y Multi-Ciudad         ║
╚══════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import asyncio
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json
import re
import requests

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# ─── MAPEO DE CATEGORÍAS A SECTORES ──────────────────────────

CATEGORY_TO_SECTOR = {
    # Odontología
    "odontología": "odontologia",
    "dentista": "odontologia",
    "clínica dental": "odontologia",
    "dental": "odontologia",
    "ortodoncista": "odontologia",
    "periodoncista": "odontologia",
    "endodoncista": "odontologia",

    # Medicina
    "médico": "medicina",
    "clínica": "medicina",
    "hospital": "medicina",
    "centro médico": "medicina",
    "consultorio médico": "medicina",
    "clínica médica": "medicina",
    "especialista médico": "medicina",
    "dermatólogo": "medicina",
    "cardiólogo": "medicina",
    "pediatra": "medicina",
    "psicólogo": "medicina",
    "fisioterapeuta": "medicina",
    "oftalmólogo": "medicina",
    "óptica": "medicina",

    # Gastronomía
    "restaurante": "gastronomia",
    "café": "gastronomia",
    "cafetería": "gastronomia",
    "bar": "gastronomia",
    "pizzería": "gastronomia",
    "comida rápida": "gastronomia",
    "delivery": "gastronomia",
    "catering": "gastronomia",
    "pastelería": "gastronomia",
    "panadería": "gastronomia",
    "food truck": "gastronomia",
    "marisquería": "gastronomia",
    "buffet": "gastronomia",

    # Manufactura/Comercio
    "ferretería": "pyme_general",
    "tienda": "pyme_general",
    "comercio": "pyme_general",
    "empresa": "pyme_general",
    "negocio": "pyme_general",
    "fábrica": "manufactura",
    "manufactura": "manufactura",
    "industria": "manufactura",
    "producción": "manufactura",
    "planta industrial": "manufactura",
    "taller": "manufactura",
}

# ─── CONFIGURACIÓN DE BÚSQUEDA ───────────────────────────────

class FlexibleLeadSearchConfig:
    """Configuración para búsqueda flexible de leads"""

    def __init__(
        self,
        ciudad: str,
        categoria: str,
        sector: str,
        resultado_maximo: int = 50,
        incluir_contacto: bool = True,
        incluir_web: bool = True,
        incluir_rating: bool = True,
        timeout: int = 30
    ):
        self.ciudad = ciudad
        self.categoria = categoria
        self.sector = sector
        self.resultado_maximo = resultado_maximo
        self.incluir_contacto = incluir_contacto
        self.incluir_web = incluir_web
        self.incluir_rating = incluir_rating
        self.timeout = timeout
        self.query = f"{categoria} en {ciudad}"

# ─── FUNCIONES DE BÚSQUEDA ───────────────────────────────────

def mapear_categoria_a_sector(categoria: str) -> Optional[str]:
    """
    Mapea una categoría a un sector del Calificador de Leads
    """
    categoria_lower = categoria.lower().strip()

    # Búsqueda exacta
    if categoria_lower in CATEGORY_TO_SECTOR:
        return CATEGORY_TO_SECTOR[categoria_lower]

    # Búsqueda parcial (contiene)
    for clave, sector in CATEGORY_TO_SECTOR.items():
        if clave in categoria_lower or categoria_lower in clave:
            return sector

    # Por defecto: PYME general
    return "pyme_general"


def limpiar_telefono(telefono: str) -> str:
    """Limpia y normaliza números telefónicos"""
    if not telefono:
        return ""
    # Elimina caracteres no numéricos excepto +
    limpio = re.sub(r'[^\d+]', '', str(telefono))
    return limpio


def extraer_url(texto: str) -> str:
    """Extrae URL de un texto"""
    if not texto:
        return ""
    # Patrón simple para URLs
    patron = r'https?://[^\s]+'
    match = re.search(patron, str(texto))
    return match.group(0) if match else ""


def crear_datos_lead_dummy(
    nombre: str,
    ciudad: str,
    categoria: str,
    telefono: str = "",
    direccion: str = "",
    sitio_web: str = "",
    rating: float = 0.0,
    reviews: int = 0
) -> Dict:
    """
    Crea un registro de lead con datos estructurados
    """
    return {
        "nombre_empresa": nombre,
        "ciudad": ciudad,
        "categoria": categoria,
        "telefono": limpiar_telefono(telefono),
        "direccion": direccion,
        "sitio_web": sitio_web,
        "rating": float(rating) if rating else 0.0,
        "numero_reviews": int(reviews) if reviews else 0,
        "fecha_busqueda": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "tamaño": "1-10",
        "redes_sociales": "desactualizado" if sitio_web else "no_tiene",
        "sitio_web_estado": "sitio_moderno" if sitio_web else "sin_sitio"
    }


def buscar_leads_mock(
    config: FlexibleLeadSearchConfig,
    progress_callback=None
) -> Tuple[pd.DataFrame, Dict]:
    """
    Versión simulada de búsqueda (para desarrollo/testing)
    Genera datos realistas de ejemplo
    """

    datos_ejemplo = {
        "restaurante": [
            {"nombre": "La Cevichería Cartagena", "telefono": "3125551234", "direccion": "Calle 3 #4-56", "web": "www.lacevicheria.co", "rating": 4.8},
            {"nombre": "Casa Vieja Restaurante", "telefono": "3015552345", "direccion": "Calle 5 #7-89", "web": "", "rating": 4.5},
            {"nombre": "El Patio Gourmet", "telefono": "3105553456", "direccion": "Av. Paseo Bolívar", "web": "www.elpatiogourmet.com", "rating": 4.7},
            {"nombre": "Sabores del Caribe", "telefono": "3125554567", "direccion": "Centro Histórico", "web": "", "rating": 4.6},
            {"nombre": "Restaurante Bahía", "telefono": "3015555678", "direccion": "Barrio Getsemaní", "web": "www.bahiarest.co", "rating": 4.4},
        ],
        "odontología": [
            {"nombre": "Clínica Dental Sonrisa Plus", "telefono": "3125556789", "direccion": "Calle 8 #10-11", "web": "www.sonrisaplus.co", "rating": 4.9},
            {"nombre": "Centro Odontológico Cartagena", "telefono": "3015556890", "direccion": "Av. San Martín", "web": "", "rating": 4.3},
            {"nombre": "Dr. Rodríguez Odontología", "telefono": "3105557901", "direccion": "Calle 5 #3-45", "web": "www.drodriguez.co", "rating": 4.7},
            {"nombre": "Dental Care Cartagena", "telefono": "3125558012", "direccion": "Centro comercial Paseo", "web": "www.dentalcare.co", "rating": 4.5},
        ],
        "médico": [
            {"nombre": "Clínica Madre Bernarda", "telefono": "3125559123", "direccion": "Av. San Martín 8-77", "web": "www.madrebernarda.co", "rating": 4.8},
            {"nombre": "Centro Médico Integral", "telefono": "3015550234", "direccion": "Calle 10 #5-67", "web": "", "rating": 4.4},
            {"nombre": "Consultorio Dr. García", "telefono": "3105551345", "direccion": "Torre Médica Cartagena", "web": "www.drgarcia.co", "rating": 4.6},
            {"nombre": "Clínica Especializada Cartagena", "telefono": "3125552456", "direccion": "Barrio Crespo", "web": "", "rating": 4.5},
        ],
        "ferretería": [
            {"nombre": "Ferretería La Construcción", "telefono": "3125553567", "direccion": "Calle 15 #20-30", "web": "", "rating": 4.2},
            {"nombre": "Materiales para la Construcción Jhon", "telefono": "3015554678", "direccion": "Av. Paseo Bolívar", "web": "www.ferreteriajhon.co", "rating": 4.1},
            {"nombre": "Ferretería Cartagena Plus", "telefono": "3105555789", "direccion": "Calle 17 #25-45", "web": "", "rating": 3.9},
            {"nombre": "Construfácil Cartagena", "telefono": "3125556890", "direccion": "Centro comercial Boquilla", "web": "www.construfacil.co", "rating": 4.0},
        ],
        "óptica": [
            {"nombre": "Óptica Visión 20/20", "telefono": "3125557901", "direccion": "Calle 8 #4-89", "web": "www.vision2020.co", "rating": 4.7},
            {"nombre": "Óptica Cartagena Premium", "telefono": "3015558012", "direccion": "Centro comercial Paseo", "web": "", "rating": 4.5},
            {"nombre": "Dr. Oftalmología + Óptica", "telefono": "3105559123", "direccion": "Av. San Martín", "web": "www.droftalmo.co", "rating": 4.6},
        ],
    }

    resultados = []
    categoria_lower = config.categoria.lower()

    ejemplos = datos_ejemplo.get(categoria_lower, [])
    if not ejemplos:
        for clave, datos in datos_ejemplo.items():
            if clave in categoria_lower or categoria_lower in clave:
                ejemplos = datos
                break

    if not ejemplos:
        ejemplos = [
            {"nombre": f"{config.categoria.title()} {config.ciudad} #{i}",
             "telefono": f"300{1000000 + i}",
             "direccion": f"Calle {i} #1-00",
             "web": f"www.ejemplo{i}.co" if i % 2 == 0 else "",
             "rating": 4.0 + (i * 0.1)}
            for i in range(1, 6)
        ]

    for ejemplo in ejemplos:
        lead = crear_datos_lead_dummy(
            nombre=ejemplo["nombre"],
            ciudad=config.ciudad,
            categoria=config.categoria,
            telefono=ejemplo["telefono"],
            direccion=ejemplo["direccion"],
            sitio_web=ejemplo["web"],
            rating=ejemplo["rating"]
        )
        resultados.append(lead)

    df = pd.DataFrame(resultados)
    estadisticas = {
        "estado": "completado",
        "total_leads": len(resultados),
        "ciudad": config.ciudad,
        "categoria": config.categoria,
        "sector_asignado": config.sector,
        "metodo": "datos_ejemplo"
    }

    return df, estadisticas


def buscar_leads_google_places(
    config: FlexibleLeadSearchConfig,
    api_key: str,
    progress_callback=None
) -> Tuple[pd.DataFrame, Dict]:
    """
    Busca leads usando Google Places API (New)
    """

    resultados = []
    estadisticas = {
        "estado": "en_progreso",
        "total_leads": 0,
        "ciudad": config.ciudad,
        "categoria": config.categoria,
        "sector_asignado": config.sector,
        "metodo": "google_places_api"
    }

    try:
        query_text = f"{config.categoria} en {config.ciudad}"
        url = "https://places.googleapis.com/v1/places:searchText"

        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key
        }

        payload = {
            "textQuery": query_text,
            "maxResultCount": min(config.resultado_maximo, 20)
        }

        if progress_callback:
            progress_callback(f"Buscando {query_text}...")

        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        places = data.get("places", [])

        if progress_callback:
            progress_callback(f"Encontrados {len(places)} resultados")

        for idx, place in enumerate(places):
            try:
                nombre = place.get("displayName", {}).get("text", f"Negocio {idx + 1}")
                telefono = ""
                if "internationalPhoneNumber" in place:
                    telefono = place["internationalPhoneNumber"]
                elif "nationalPhoneNumber" in place:
                    telefono = place["nationalPhoneNumber"]

                direccion = place.get("formattedAddress", "")
                sitio_web = place.get("websiteUri", "")
                rating = place.get("rating", 0.0)
                reviews = place.get("userRatingCount", 0)

                lead = crear_datos_lead_dummy(
                    nombre=nombre,
                    ciudad=config.ciudad,
                    categoria=config.categoria,
                    telefono=telefono,
                    direccion=direccion,
                    sitio_web=sitio_web,
                    rating=rating,
                    reviews=reviews
                )

                resultados.append(lead)

                if progress_callback:
                    progress_callback(f"Procesados {len(resultados)} leads...")

            except Exception as e:
                print(f"Error procesando lugar {idx}: {e}")
                continue

        estadisticas["estado"] = "completado"
        estadisticas["total_leads"] = len(resultados)

    except requests.exceptions.HTTPError as e:
        estadisticas["estado"] = "error"
        estadisticas["mensaje"] = f"Error HTTP {e.response.status_code}: {e.response.text}"
        estadisticas["total_leads"] = len(resultados)
    except requests.exceptions.RequestException as e:
        estadisticas["estado"] = "error"
        estadisticas["mensaje"] = f"Error en la solicitud: {str(e)}"
        estadisticas["total_leads"] = len(resultados)
    except Exception as e:
        estadisticas["estado"] = "error"
        estadisticas["mensaje"] = str(e)
        estadisticas["total_leads"] = len(resultados)

    if resultados:
        df = pd.DataFrame(resultados)
        df = df.sort_values("rating", ascending=False)
        return df, estadisticas
    else:
        return pd.DataFrame(), estadisticas


def buscar_leads(
    ciudad: str,
    categoria: str,
    resultado_maximo: int = 50,
    usar_mock: bool = False,
    api_key: str = "",
    progress_callback=None
) -> Tuple[pd.DataFrame, Dict]:
    """
    Función principal de búsqueda de leads
    """

    sector = mapear_categoria_a_sector(categoria)
    config = FlexibleLeadSearchConfig(
        ciudad=ciudad,
        categoria=categoria,
        sector=sector,
        resultado_maximo=resultado_maximo
    )

    # Modo 1: Usuario pidió datos de ejemplo explícitamente
    if usar_mock:
        df, stats = buscar_leads_mock(config, progress_callback)
        return df, stats

    # Modo 2: Intentar Google Places API con fallback automático
    if api_key and api_key.strip():
        df, stats = buscar_leads_google_places(config, api_key, progress_callback)

        # Si Google Places falló, fallback a datos de ejemplo
        if stats.get("estado") == "error" or df.empty:
            if progress_callback:
                progress_callback("Usando datos de ejemplo como fallback...")
            df, fallback_stats = buscar_leads_mock(config, progress_callback)
            fallback_stats["metodo_original"] = "google_places_api"
            fallback_stats["metodo_actual"] = "datos_ejemplo_fallback"
            fallback_stats["razon_fallback"] = stats.get("mensaje", "Error en API")
            return df, fallback_stats
        return df, stats

    # Modo 3: Sin API key, usar datos de ejemplo
    df, stats = buscar_leads_mock(config, progress_callback)
    return df, stats


def exportar_leads(
    df: pd.DataFrame,
    ciudad: str,
    categoria: str,
    formato: str = "csv"
) -> bytes:
    """
    Exporta los leads en formato CSV o Excel
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if formato == "csv":
        return df.to_csv(index=False).encode('utf-8')
    elif formato == "excel":
        import io
        output = io.BytesIO()
        df.to_excel(output, index=False, sheet_name="Leads")
        output.seek(0)
        return output.getvalue()

    return b""
